# Hackathon Bus Reservation System

Flask web app for managing bus seat reservations (48 seats: 12 rows × 4 columns).

## Features

- Student seat reservation with column-based pricing
- Admin dashboard with seating chart and sales tracking
- E-ticket generation and reservation management
- Responsive, JS-backed page features (idk if that was allowed but I couldn't figure it out in python)

## Quick Start

```bash
# Run
docker-compose up --build
```

Visit `http://localhost:4320`

## Tech Stack

- Python 3.12 | Flask | SQLAlchemy | SQLite | Bootstrap 5 | Docker

## Database Schema

**Reservations**: id, passengerName, seatRow, seatColumn, eTicketNumber, created
**Admins**: username, password (pre-seeded)

## Routes

- `/` - Main menu
- `/reserve` - Reservation form
- `/admin` - Admin login
- `/admin/dashboard` - Seating chart & sales
- `/admin/delete/<id>` - Delete reservation
- `/admin/logout` - Admin logout

## Seat Pricing

- Columns 1 & 4 (Window): $100
- Column 2 (Left Aisle): $75
- Column 3 (Right Aisle): $50

## Development

- Branch: `feature/<name>`, `bugfix/<name>`, `docs/<name>`
- Code formatting: Black (100 char lines) & Ruff linting
- Use # for comments, add docstrings, follow PEP 8
- Update docs when adding features
- Database is tracked in git (intentional)
