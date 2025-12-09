# Hackathon Bus Reservation System

Flask web app for managing bus seat reservations (48 seats: 12 rows × 4 columns).

## Features

- Student seat reservation with zone-based pricing
- Admin dashboard with seating chart and sales tracking
- E-ticket generation and reservation management

## Quick Start

```bash
# Setup
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
pip install -r requirements.txt

# Run
python app.py
```

Visit `http://127.0.0.1:5000`

## Tech Stack

- Python 3.8+ | Flask | SQLAlchemy | SQLite | Bootstrap 5

## Database Schema

**Reservations**: id, passengerName, seatRow, seatColumn, eTicketNumber, created
**Admins**: username, password (pre-seeded)

## Routes

- `/` - Main menu
- `/reserve` - Reservation form
- `/admin/login` - Admin login
- `/admin/dashboard` - Seating chart & sales
- `/admin/delete/<id>` - Delete reservation

## Pricing Zones

- Rows 1-4: Premium ($30)
- Rows 5-8: Standard ($20)
- Rows 9-12: Economy ($15)

## Development

- Branch: `feature/<name>`, `bugfix/<name>`, `docs/<name>`
- Code formatting: Black (100 char lines) & Ruff linting
- Use # for comments, add docstrings, follow PEP 8
- Update docs when adding features
- Database is tracked in git (intentional)

### Code Quality Tools

```bash
# Format code
black --line-length 100 .

# Lint code
ruff check .
ruff check --fix .
```

## Project Status

### Completed ✅
- [x] Core business logic (seat pricing, ticket generation, availability check, sales calculation)
- [x] Database schema and SQLAlchemy models
- [x] Code formatting tools (Black & Ruff)
- [x] Documentation (README, CONTRIBUTING, TODO.md)
- [x] HTML templates with Bootstrap 5 and Mizzou theming
- [x] Responsive seating chart visualization (CSS Grid)
- [x] Interactive seat selection with JavaScript
- [x] Admin dashboard interface

### To-Do
- [ ] Backend route integration (render_template, POST handlers)
- [ ] Admin authentication logic (session management)
- [ ] Form validation and error handling
- [ ] Database integration with templates
