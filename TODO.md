# Bus Reservation System - TODO List

## Project Status Tracker

### Team Contributions
| Task                    | Assigned To | Status | Notes                                    |
|-------------------------|-------------|--------|------------------------------------------|
| Helper Functions        | Jackson     | Done   | All 4 functions implemented              |
| Templates & CSS         | Claude      | Done   | 5 templates + style.css with Mizzou theme |
| Backend Integration     |             | Todo   | Connect templates to routes              |
| Admin Authentication    |             | Todo   | Session management implementation        |

---

## 1. Core Business Logic Implementation ✅ COMPLETED

### Helper Functions (in app.py)

- [x] **Implement `calculate_seat_price(row)`**
  - Zone-based pricing: Front $30, Middle $20, Back $15
  - Input validation for rows 1-12
  - Returns float price value

- [x] **Implement `generate_ticket_number()`**
  - Format: HACK-XXXX-XXXX (random 8-digit code)
  - Uniqueness verified against database
  - Regenerates on collision

- [x] **Implement `is_seat_available(row, column)`**
  - Queries Reservation model for seat at (row, column)
  - Input validation for row (1-12) and column (1-4)
  - Returns True if available, False if reserved

- [x] **Implement `get_total_sales()`**
  - Queries all reservations from database
  - Calculates price for each seat using `calculate_seat_price()`
  - Returns total revenue sum as float

---

## 2. Template Development ✅ COMPLETED

### Base Template

- [x] **Create `templates/base.html`**
  - Include Bootstrap 5 CDN links
  - Create navigation bar with link to home (/)
  - Define block content area
  - Add footer if desired
  - Flash message system integrated
  - Mizzou gold (#F1B82D) themed navbar

### Page Templates

- [x] **Create `templates/index.html`**
  - Extend base.html
  - Display welcome message with hero section
  - Links to /reserve and /admin (styled CTA cards)
  - Zone pricing information table
  - Replace inline HTML in `/` route

- [x] **Create `templates/reserve.html`**
  - Extend base.html
  - Reservation form (passenger name, seat selection)
  - Interactive seat grid showing availability (12 rows × 4 columns)
  - Display pricing by zone with color coding
  - JavaScript for seat selection and price calculation
  - Show success/error messages
  - Replace inline HTML in `/reserve` route

- [x] **Create `templates/admin_login.html`**
  - Extend base.html
  - Login form (username, password)
  - Error message display for failed login
  - Mizzou gold top border styling
  - Replace inline HTML in `/admin` route

- [x] **Create `templates/admin_dashboard.html`**
  - Extend base.html
  - Display seating chart (12×4 grid with color coding)
  - Statistics badges (total sales, seats reserved, seats available)
  - Show total sales from `get_total_sales()`
  - List all reservations in responsive table format
  - Delete button for each reservation with confirmation
  - Hover tooltips on reserved seats showing passenger names
  - Replace inline HTML in `/admin/dashboard` route

---

## 3. Frontend Styling ✅ COMPLETED

### CSS Development

- [x] **Create `static/style.css`**
  - CSS variables for Mizzou color palette (gold #F1B82D, black, green, red, blue)
  - Seating chart CSS Grid layout (12 rows × 4 columns)
  - Color coding: green (available), red (reserved), blue (selected)
  - Zone pricing visual indicators with light gold backgrounds
  - Responsive design with breakpoints (60px → 50px → 45px seats)
  - Custom Mizzou-themed styling to complement Bootstrap 5
  - Interactive hover effects and transitions
  - Admin dashboard statistics badges and table styling

---

## 4. Route Logic Implementation

### Reservation Routes

- [ ] **Update `/reserve` GET handler**
  - Query all reservations to determine seat availability
  - Pass availability data to template
  - Render reserve.html template

- [ ] **Update `/reserve` POST handler**
  - Validate form input (passenger name, seat selection)
  - Check seat availability using `is_seat_available()`
  - Generate ticket number using `generate_ticket_number()`
  - Create and save new Reservation to database
  - Handle errors (seat taken, validation failures)
  - Render template with success/error messages

### Admin Routes

- [ ] **Update `/admin` GET handler**
  - Render admin_login.html template

- [ ] **Update `/admin` POST handler**
  - Validate credentials against Admin model
  - Set Flask session on successful login
  - Redirect to /admin/dashboard
  - Show error message on failed login

- [ ] **Update `/admin/dashboard` GET handler**
  - Implement session authentication check
  - Redirect to /admin if not authenticated
  - Query all reservations
  - Calculate total sales using `get_total_sales()`
  - Render admin_dashboard.html with data

- [ ] **Update `/admin/delete/<id>` handler**
  - Implement session authentication check
  - Find reservation by ID
  - Delete from database
  - Redirect back to dashboard
  - Handle errors (reservation not found)

---

## 5. Authentication & Security

- [ ] **Implement session-based authentication**
  - Set up Flask secret_key for sessions
  - Create login_required decorator or checks
  - Apply to admin routes (/admin/dashboard, /admin/delete)

- [ ] **Add security measures**
  - Password hashing verification for admin login
  - CSRF protection if needed
  - Input validation and sanitization

---

## 6. Testing

- [ ] **Test reservation flow**
  - Navigate to /reserve
  - Select available seat
  - Submit reservation with valid name
  - Verify seat appears as reserved
  - Verify e-ticket number generated

- [ ] **Test seat availability**
  - Try to book same seat twice
  - Verify error message appears
  - Verify database not updated

- [ ] **Test admin login**
  - Login with correct credentials
  - Verify dashboard access
  - Login with incorrect credentials
  - Verify error message

- [ ] **Test admin dashboard**
  - Verify seating chart displays correctly
  - Verify reserved seats highlighted
  - Verify total sales calculation
  - Verify reservation list displays

- [ ] **Test reservation deletion**
  - Delete reservation from admin dashboard
  - Verify seat becomes available again
  - Verify sales total updates

- [ ] **Test edge cases**
  - Empty passenger name
  - Invalid seat selection
  - Session expiration
  - Direct URL access to admin routes without login

---

## 7. Documentation IN PROCESS

- [IP] **Update README.md**
  - Installation instructions included
  - Running instructions included
  - Feature overview complete
  - Project status section updated with completed templates
  - Black and Ruff tools documented
  - Template implementation marked as complete

- [IP] **Update CONTRIBUTING.md**
  - Code style guidelines (PEP 8)
  - Black and Ruff integration added
  - Branch strategy documented
  - PR process defined
  - Pre-commit workflow established
  - IDE integration instructions

- [IP] **Update TODO.md**
  - Template development section marked complete
  - Frontend styling section marked complete
  - Team contributions table updated
  - Documentation section updated

- [IP] **Add code comments**
  - Docstrings for all helper functions
  - Inline comments for business logic
  - PEP 8 compliant formatting
  - HTML template comments for sections

---

## 8. Final Polish

- [ ] **Code review**
  - PEP 8 compliance check
  - Remove any debug print statements
  - Verify 100 character line limit
  - Ensure consistent indentation (4 spaces)

- [ ] **Browser testing**
  - Test in Chrome
  - Test in Firefox
  - Test responsive design on mobile

- [ ] **Database verification**
  - Ensure schema.sql matches models
  - Verify admin accounts exist
  - Test with clean database

---

## Optional Enhancements (If Time Permits)

- [ ] Add passenger contact information (email/phone)
- [ ] Email confirmation with e-ticket
- [ ] Seat selection dropdown vs. grid click
- [ ] Filter/search reservations in admin
- [ ] Export reservations to CSV
- [ ] Add reservation timestamps to display
- [ ] Logout functionality for admin
- [ ] Better error handling and user feedback

---

## Notes

- Database (reservations.db) is tracked in git
- Admin credentials are pre-seeded (check database)
- Use Bootstrap 5 for all templates
- All templates must extend base.html
- Use # for comments, not """
