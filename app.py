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
        except (ValueError, TypeError):
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

        # Generate ticket and create reservation (store as 0-based in database)
        ticket_number = generate_ticket_number(passenger_name)
        new_reservation = Reservation(
            passengerName=passenger_name,
            seatRow=seat_row,
            seatColumn=seat_column,
            eTicketNumber=ticket_number,
        )

        db.session.add(new_reservation)
        db.session.commit()

        # Calculate price for confirmation message (using 0-based row and column)
        price = calculate_seat_price(seat_row, seat_column)

        flash(
            f"Reservation successful! {passenger_name}, your seat {seat_row_display}-{seat_column_display} "
            f"(${price:.2f}) is confirmed. E-Ticket: {ticket_number}",
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
    reserved_count = Reservation.query.count()
    available_count = total_seats - reserved_count
    total_sales = get_total_sales()

    # Get seat data
    availability = get_seat_availability_grid()
    seat_names = get_seat_names_grid()

    # Get all reservations sorted by creation date (oldest first)
    reservations = Reservation.query.order_by(Reservation.created.asc()).all()

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

    # Find and delete reservation
    reservation = Reservation.query.get(reservation_id)

    if reservation:
        passenger = reservation.passengerName
        seat = f"{reservation.seatRow}-{reservation.seatColumn}"

        db.session.delete(reservation)
        db.session.commit()

        flash(f"Reservation for {passenger} (Seat {seat}) has been deleted.", "success")
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


def get_seat_availability_grid():
    """
    Build a 12×4 grid showing seat availability status

    Returns:
        list: 2D list where availability[row][col] is True (available) or False (reserved)
              Uses 0-based indexing (row 0-11, col 0-3)
    """
    # Initialize all seats as available
    availability = [[True for _ in range(4)] for _ in range(12)]

    # Mark reserved seats (database uses 0-based indexing)
    reservations = Reservation.query.all()
    for reservation in reservations:
        # Validate indices before using them
        if 0 <= reservation.seatRow <= 11 and 0 <= reservation.seatColumn <= 3:
            availability[reservation.seatRow][reservation.seatColumn] = False

    return availability


def get_seat_names_grid():
    """
    Build a 12×4 grid showing passenger names for reserved seats

    Returns:
        list: 2D list where seat_names[row][col] is passenger name or None
              Uses 0-based indexing (row 0-11, col 0-3)
    """
    # Initialize empty grid
    seat_names = [[None for _ in range(4)] for _ in range(12)]

    # Fill in passenger names (database uses 0-based indexing)
    reservations = Reservation.query.all()
    for reservation in reservations:
        # Validate indices before using them
        if 0 <= reservation.seatRow <= 11 and 0 <= reservation.seatColumn <= 3:
            seat_names[reservation.seatRow][reservation.seatColumn] = reservation.passengerName

    return seat_names


# Run the application
if __name__ == "__main__":
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Run in debug mode for development
    app.run(debug=True, host="0.0.0.0", port=5000)
