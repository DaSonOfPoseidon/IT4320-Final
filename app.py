# Hackathon Bus Reservation System
# Flask web application for managing bus seat reservations

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "tigolbitties")  # Change in production!

# Use absolute path to database file in the project root
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'reservations.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Database Models
class Reservation(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    passengerName = db.Column(db.Text, nullable=False)
    seatRow = db.Column(db.Integer, nullable=False)
    seatColumn = db.Column(db.Integer, nullable=False)
    eTicketNumber = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Reservation {self.passengerName} - Seat {self.seatRow}-{self.seatColumn}>"


class Admin(db.Model):
    __tablename__ = "admins"
    username = db.Column(db.Text, primary_key=True)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Admin {self.username}>"


# Routes
@app.route("/")
def index():
    """Main menu - home page"""
    # Calculate available seats
    total_seats = 48
    reserved_count = Reservation.query.count()
    available_count = total_seats - reserved_count

    return render_template("index.html", available_count=available_count, total_seats=total_seats)


@app.route("/reserve", methods=["GET", "POST"])
def reserve():
    """Reservation form page"""
    if request.method == "POST":
        # Get form data
        passenger_name = request.form.get("passenger_name", "").strip()
        seat_row_display = request.form.get("seat_row")
        seat_column_display = request.form.get("seat_column")

        # Validate passenger name
        if not passenger_name or len(passenger_name) < 2 or len(passenger_name) > 50:
            flash("Passenger name must be between 2 and 50 characters.", "danger")
            return redirect(url_for("reserve"))

        # Validate seat coordinates and convert from 1-based (display) to 0-based (database)
        try:
            seat_row_display = int(seat_row_display)
            seat_column_display = int(seat_column_display)

            # Convert to 0-based indexing for database
            seat_row = seat_row_display - 1
            seat_column = seat_column_display - 1
        except:
            flash("Invalid seat selection. Please select a seat.", "danger")
            return redirect(url_for("reserve"))

        # Check if seat is available (using 0-based indexing)
        if not is_seat_available(seat_row, seat_column):
            flash(
                f"Seat {seat_row_display}-{seat_column_display} is no longer available. "
                "Please select another seat.",
                "warning",
            )
            return redirect(url_for("reserve"))

        reservation, error = create_reservation(passenger_name, seat_row, seat_column)
        if error:
            flash(error, "danger")
            return redirect(url_for("reserve"))

        price = calculate_seat_price(seat_row, seat_column)

        flash(
            f"Reservation successful! {passenger_name}, your seat {seat_row_display}-{seat_column_display} "
            f"(${price:.2f}) is confirmed. E-Ticket: {reservation.eTicketNumber}",
            "success",
        )
        return redirect(url_for("index"))

    # GET request - show form
    availability = get_seat_availability_grid()
    return render_template("reserve.html", availability=availability)



@app.route("/admin", methods=["GET", "POST"])
def admin():
    """Admin login page"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Validate credentials
        admin_user = Admin.query.filter_by(username=username).first()

        if admin_user and admin_user.password == password:
            # Set session
            session["admin_logged_in"] = True
            session["admin_username"] = username
            flash(f"Welcome, {username}!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("admin"))

    # GET request - show login form
    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    """Admin dashboard - seating chart and reservations"""
    # Check authentication
    if not session.get("admin_logged_in"):
        flash("Please log in to access the admin dashboard.", "warning")
        return redirect(url_for("admin"))

    # Calculate statistics
    total_seats = 48
    reserved_list = get_all_reservations()
    reserved_count = len(reserved_list)
    available_count = total_seats - reserved_count
    total_sales = get_total_sales()

    # Get seat data
    availability = get_seat_availability_grid()
    seat_names = get_seat_names_grid()

    reservations = sorted(reserved_list, key=lambda r: r.created)

    return render_template(
        "admin_dashboard.html",
        total_sales=total_sales,
        reserved_count=reserved_count,
        total_seats=total_seats,
        available_count=available_count,
        availability=availability,
        seat_names=seat_names,
        reservations=reservations,
    )



@app.route("/admin/delete/<int:reservation_id>", methods=["POST"])
def admin_delete(reservation_id):
    """Delete a reservation"""
    # Check authentication
    if not session.get("admin_logged_in"):
        flash("Please log in to access the admin dashboard.", "warning")
        return redirect(url_for("admin"))

    reservation = get_reservation_by_id(reservation_id)

    if reservation:
        passenger = reservation.passengerName
        seat = f"{reservation.seatRow}-{reservation.seatColumn}"
        success, error = delete_reservation(reservation_id)
        if success:
            flash(f"Reservation for {passenger} (Seat {seat}) has been deleted.", "success")
        else:
            flash(error, "danger")
    else:
        flash("Reservation not found.", "danger")

    return redirect(url_for("admin_dashboard"))



@app.route("/admin/logout")
def admin_logout():
    """Log out admin user"""
    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


# Helper functions


def get_cost_matrix():
    """
    Get the seat pricing cost matrix

    Returns:
        list: 12x4 matrix where cost_matrix[row][col] is the price for that seat
    """
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix


def calculate_seat_price(row, column):
    """
    Calculate the price of a seat based on its position using cost matrix

    Args:
        row (int): The row number (0-11, 0-based index)
        column (int): The column number (0-3, 0-based index)

    Returns:
        float: The price for the seat
    """
    # Input validation
    if row < 0 or row > 11:
        raise ValueError("Row must be between 0 and 11")
    if column < 0 or column > 3:
        raise ValueError("Column must be between 0 and 3")

    # Get price from cost matrix
    cost_matrix = get_cost_matrix()
    return float(cost_matrix[row][column])


def generate_ticket_number(passenger_name):
    """
    Generate e-ticket number based on passenger name

    Pattern: Interleave passenger name letters with "INFOTC4320"
    Example: "Alice" -> AIlNiFcOeTC4320

    Args:
        passenger_name (str): Passenger's full name

    Returns:
        str: E-ticket number based on passenger name
    """
    # Remove all whitespace from name
    passenger_name = passenger_name.replace(" ", "")

    separator_string = "INFOTC4320"

    # Start with first letter (uppercase)
    ticket = passenger_name[0].upper()

    # Get remaining letters (lowercase)
    remaining_letters = passenger_name[1:].lower()

    # Interleave remaining letters with separator string
    max_length = max(len(remaining_letters), len(separator_string))
    for i in range(max_length):
        if i < len(separator_string):
            ticket += separator_string[i]
        if i < len(remaining_letters):
            ticket += remaining_letters[i]

    return ticket


def is_seat_available(row, column):
    """
    Check if a seat is available for reservation

    Args:
        row (int): Seat row (0-11, 0-based index)
        column (int): Seat column (0-3, 0-based index)

    Returns:
        bool: True if available, False if taken
    """
    # Input validation
    if row < 0 or row > 11:
        raise ValueError("Row must be between 0 and 11")
    if column < 0 or column > 3:
        raise ValueError("Column must be between 0 and 3")

    # Check if seat is already reserved
    reservation = Reservation.query.filter_by(seatRow=row, seatColumn=column).first()

    return reservation is None


def get_total_sales():
    """
    Calculate total sales from all reservations

    Returns:
        float: Total sales amount
    """
    total = 0.0

    # Get all reservations
    reservations = Reservation.query.all()

    # Calculate price for each reservation using row and column
    for reservation in reservations:
        price = calculate_seat_price(reservation.seatRow, reservation.seatColumn)
        total += price

    return total

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_database():
    """Initialize database with tables and default admin"""
    with app.app_context():
        db.create_all()
        
        # Create default admin if none exists
        if Admin.query.count() == 0:
            default_admin = Admin(username="admin", password="password")
            db.session.add(default_admin)
            db.session.commit()
            print("Default admin created: username='admin', password='password'")
            print("IMPORTANT: Change this password in production!")

# =============================================================================================
#   Database operations
# =============================================================================================

def create_reservation(passenger_name, seat_row, seat_column):
    """
    Create a new reservation (CREATE operation)
    
    Args:
        passenger_name (str): Full name of passenger
        seat_row (int): Seat row (0-11, 0-based index)
        seat_column (int): Seat column (0-3, 0-based index)
    
    Returns:
        tuple: (reservation, error_message)
            - reservation: Reservation object if successful, None if error
            - error_message: None if successful, error string if error
    """
    try:
        # Validate passenger name
        if not passenger_name or not isinstance(passenger_name, str):
            return None, "Passenger name is required"
        
        passenger_name = passenger_name.strip()
        
        if len(passenger_name) < 2:
            return None, "Passenger name must be at least 2 characters"
        
        if len(passenger_name) > 100:
            return None, "Passenger name must be less than 100 characters"
        
        # Validate seat position (0-based indexing)
        if not isinstance(seat_row, int) or not isinstance(seat_column, int):
            return None, "Seat row and column must be integers"
        
        if not (0 <= seat_row <= 11):
            return None, "Seat row must be between 0 and 11"
        
        if not (0 <= seat_column <= 3):
            return None, "Seat column must be between 0 and 3"
        
        # Check seat availability
        if not is_seat_available(seat_row, seat_column):
            return None, f"Seat {seat_row}-{seat_column} is already reserved"
        
        # Generate unique ticket number
        ticket_number = generate_ticket_number(passenger_name)
        
        # Ensure ticket number is unique (edge case: similar names)
        counter = 1
        original_ticket = ticket_number
        while Reservation.query.filter_by(eTicketNumber=ticket_number).first():
            ticket_number = f"{original_ticket}{counter}"
            counter += 1
        
        # Create reservation object
        reservation = Reservation(
            passengerName=passenger_name,
            seatRow=seat_row,
            seatColumn=seat_column,
            eTicketNumber=ticket_number
        )
        
        # Save to database
        db.session.add(reservation)
        db.session.commit()
        
        return reservation, None
        
    except ValueError as e:
        db.session.rollback()
        return None, f"Validation error: {str(e)}"
    except Exception as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}"


def get_all_reservations():
    """
    Retrieve all reservations (READ operation)
    
    Returns:
        list: List of Reservation objects ordered by creation date (newest first)
    """
    try:
        return Reservation.query.order_by(Reservation.created.desc()).all()
    except Exception as e:
        print(f"Error retrieving reservations: {e}")
        return []


def get_reservation_by_id(reservation_id):
    """
    Get a specific reservation by ID (READ operation)
    
    Args:
        reservation_id (int): Primary key of reservation
    
    Returns:
        Reservation: Reservation object or None if not found
    """
    try:
        if not isinstance(reservation_id, int) or reservation_id < 1:
            return None
        return Reservation.query.get(reservation_id)
    except Exception as e:
        print(f"Error retrieving reservation {reservation_id}: {e}")
        return None


def delete_reservation(reservation_id):
    """
    Delete a reservation by ID (DELETE operation)
    
    Args:
        reservation_id (int): Primary key of reservation to delete
    
    Returns:
        tuple: (success, error_message)
            - success: True if deleted, False if error
            - error_message: None if successful, error string if error
    """
    try:
        # Validate input
        if not isinstance(reservation_id, int) or reservation_id < 1:
            return False, "Invalid reservation ID"
        
        # Find reservation
        reservation = Reservation.query.get(reservation_id)
        
        if not reservation:
            return False, "Reservation not found"
        
        # Delete from database
        db.session.delete(reservation)
        db.session.commit()
        
        return True, None
        
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"


def is_seat_available(row, column):
    """
    Check if a seat is available for reservation
    
    Args:
        row (int): Seat row (0-11, 0-based index)
        column (int): Seat column (0-3, 0-based index)
    
    Returns:
        bool: True if available, False if taken or invalid
    """
    try:
        # Input validation
        if not isinstance(row, int) or not isinstance(column, int):
            return False
        
        if row < 0 or row > 11:
            return False
        
        if column < 0 or column > 3:
            return False

        # Check if seat is already reserved
        reservation = Reservation.query.filter_by(seatRow=row, seatColumn=column).first()
        return reservation is None
        
    except Exception as e:
        print(f"Error checking seat availability: {e}")
        return False


def get_total_sales():
    """
    Calculate total sales from all reservations
    
    Returns:
        float: Total sales amount
    """
    try:
        total = 0.0
        reservations = Reservation.query.all()
        
        for reservation in reservations:
            # Validate indices before calculating price
            if 0 <= reservation.seatRow <= 11 and 0 <= reservation.seatColumn <= 3:
                price = calculate_seat_price(reservation.seatRow, reservation.seatColumn)
                total += price
        
        return total
        
    except Exception as e:
        print(f"Error calculating total sales: {e}")
        return 0.0


def get_seat_availability_grid():
    """
    Build a 12×4 grid showing seat availability status
    
    Returns:
        list: 2D list where availability[row][col] is True (available) or False (reserved)
              Uses 0-based indexing (row 0-11, col 0-3)
    """
    try:
        # Initialize all seats as available
        availability = [[True for _ in range(4)] for _ in range(12)]

        # Mark reserved seats
        reservations = Reservation.query.all()
        for reservation in reservations:
            # Validate indices before using them
            if 0 <= reservation.seatRow <= 11 and 0 <= reservation.seatColumn <= 3:
                availability[reservation.seatRow][reservation.seatColumn] = False

        return availability
        
    except Exception as e:
        print(f"Error building availability grid: {e}")
        # Return all available on error
        return [[True for _ in range(4)] for _ in range(12)]


def get_seat_names_grid():
    """
    Build a 12×4 grid showing passenger names for reserved seats
    
    Returns:
        list: 2D list where seat_names[row][col] is passenger name or None
              Uses 0-based indexing (row 0-11, col 0-3)
    """
    try:
        # Initialize empty grid
        seat_names = [[None for _ in range(4)] for _ in range(12)]

        # Fill in passenger names
        reservations = Reservation.query.all()
        for reservation in reservations:
            # Validate indices before using them
            if 0 <= reservation.seatRow <= 11 and 0 <= reservation.seatColumn <= 3:
                seat_names[reservation.seatRow][reservation.seatColumn] = reservation.passengerName

        return seat_names
        
    except Exception as e:
        print(f"Error building seat names grid: {e}")
        # Return empty grid on error
        return [[None for _ in range(4)] for _ in range(12)]


# Run the application
if __name__ == "__main__":
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Run in debug mode for development
    app.run(debug=True, host="0.0.0.0", port=5000)
