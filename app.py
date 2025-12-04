# Hackathon Bus Reservation System
# Flask web application for managing bus seat reservations

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"  # Change this in production
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reservations.db"
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
    return """
    <html>
    <head>
        <title>Bus Reservation System</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            .menu { display: flex; gap: 20px; margin-top: 30px; }
            .menu a {
                display: block;
                padding: 20px 40px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                text-align: center;
            }
            .menu a:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h1>Hackathon Bus Reservation System</h1>
        <p>Welcome! Please select an option:</p>
        <div class="menu">
            <a href="/reserve">Reserve a Seat</a>
            <a href="/admin">Admin Login</a>
        </div>
    </body>
    </html>
    """


@app.route("/reserve")
def reserve():
    """Reservation form page (to be implemented)"""
    return """
    <html>
    <head>
        <title>Reserve a Seat</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        </style>
    </head>
    <body>
        <h1>Reserve Your Seat</h1>
        <p>Reservation form coming soon...</p>
        <p><a href="/">Back to Home</a></p>
    </body>
    </html>
    """


@app.route("/admin")
def admin():
    """Admin login page (to be implemented)"""
    return """
    <html>
    <head>
        <title>Admin Login</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        </style>
    </head>
    <body>
        <h1>Admin Login</h1>
        <p>Admin login form coming soon...</p>
        <p><a href="/">Back to Home</a></p>
    </body>
    </html>
    """


# Helper functions (to be implemented by team)


def calculate_seat_price(row):
    """
    Calculate the price of a seat based on its row (zone-based pricing)

    Args:
        row (int): The row number (1-12)

    Returns:
        float: The price for the seat
    """
    # Input validation
    if row < 1 or row > 12:
        raise ValueError("Row must be between 1 and 12")

    # Zone-based pricing
    if row <= 4:
        return 30.0  # Front zone (rows 1-4)
    elif row <= 8:
        return 20.0  # Middle zone (rows 5-8)
    else:
        return 15.0  # Back zone (rows 9-12)


def generate_ticket_number():
    """
    Generate a unique e-ticket number

    Returns:
        str: Unique ticket number (e.g., HACK-1234-5678)
    """
    while True:
        # Generate two 4-digit random numbers
        part1 = random.randint(1000, 9999)
        part2 = random.randint(1000, 9999)
        ticket = f"HACK-{part1}-{part2}"

        # Check if ticket number already exists in database
        existing = Reservation.query.filter_by(eTicketNumber=ticket).first()
        if not existing:
            return ticket


def is_seat_available(row, column):
    """
    Check if a seat is available for reservation

    Args:
        row (int): Seat row (1-12)
        column (int): Seat column (1-4)

    Returns:
        bool: True if available, False if taken
    """
    # Input validation
    if row < 1 or row > 12:
        raise ValueError("Row must be between 1 and 12")
    if column < 1 or column > 4:
        raise ValueError("Column must be between 1 and 4")

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

    # Calculate price for each reservation
    for reservation in reservations:
        price = calculate_seat_price(reservation.seatRow)
        total += price

    return total


# Run the application
if __name__ == "__main__":
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Run in debug mode for development
    app.run(debug=True, host="127.0.0.1", port=5000)
