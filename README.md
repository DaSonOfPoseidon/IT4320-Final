# Hackathon Bus Reservation System

Flask web app for managing bus seat reservations (48 seats: 12 rows × 4 columns).

## Features

- Student seat reservation with zone-based pricing
- Admin dashboard with seating chart and sales tracking
- E-ticket generation and reservation management

## Quick Start

```bash
# Run
docker-compose up --build
```

Visit `http://localhost:5000`

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

- Rows 1-4: Premium
- Rows 5-8: Standard
- Rows 9-12: Economy

## Development

- Branch: `feature/<name>`, `bugfix/<name>`, `docs/<name>`
- Use # for comments, add docstrings, follow PEP 8
- Update docs when adding features
- Database is tracked in git (intentional)

## To-Do

- [ ] HTML templates with Bootstrap 5
- [ ] Reservation form + validation
- [ ] Admin authentication
- [ ] Seating chart visualization
- [ ] E-ticket generation
- [ ] Sales calculation
- [ ] Reservation deletion
