# Bus Reservation System - TODO List

## Project Status Tracker

### Team Contributions
| Task | Assigned To | Status | Notes |
|------|-------------|--------|-------|
|      |             |        |       |
|      |             |        |       |
|      |             |        |       |

---

## 1. Core Business Logic Implementation

### Helper Functions (in app.py)

- [ ] **Implement `calculate_seat_price(row)`**
  - Define pricing zones (Front: rows 1-4, Middle: rows 5-8, Back: rows 9-12)
  - Set price values for each zone
  - Return appropriate price based on row number

- [ ] **Implement `generate_ticket_number()`**
  - Generate unique format: HACK-XXXX-XXXX
  - Ensure uniqueness across all reservations
  - Use random alphanumeric characters

- [ ] **Implement `is_seat_available(row, column)`**
  - Query Reservation model for seat at (row, column)
  - Return True if available, False if reserved

- [ ] **Implement `get_total_sales()`**
  - Query all reservations from database
  - Calculate price for each seat using `calculate_seat_price()`
  - Return total revenue sum

---

## 2. Template Development

### Base Template

- [ ] **Create `templates/base.html`**
  - Include Bootstrap 5 CDN links
  - Create navigation bar with link to home (/)
  - Define block content area
  - Add footer if desired

### Page Templates

- [ ] **Create `templates/index.html`**
  - Extend base.html
  - Display welcome message
  - Links to /reserve and /admin
  - Replace inline HTML in `/` route

- [ ] **Create `templates/reserve.html`**
  - Extend base.html
  - Reservation form (passenger name, seat selection)
  - Seat grid showing availability (12 rows × 4 columns)
  - Display pricing by zone
  - Show success/error messages
  - Replace inline HTML in `/reserve` route

- [ ] **Create `templates/admin_login.html`**
  - Extend base.html
  - Login form (username, password)
  - Error message display for failed login
  - Replace inline HTML in `/admin` route

- [ ] **Create `templates/admin_dashboard.html`**
  - Extend base.html
  - Display seating chart (12×4 grid with color coding)
  - Show total sales from `get_total_sales()`
  - List all reservations in table format
  - Delete button for each reservation
  - Replace inline HTML in `/admin/dashboard` route

---

## 3. Frontend Styling

### CSS Development

- [ ] **Create `static/style.css`**
  - Seating chart CSS Grid layout (12 rows × 4 columns)
  - Color coding: green (available), red (reserved)
  - Zone pricing visual indicators
  - Responsive design considerations
  - Custom styling to complement Bootstrap

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

## 7. Documentation

- [ ] **Update README.md** (if exists)
  - Installation instructions
  - Running instructions
  - Feature overview
  - Screenshots if desired

- [ ] **Update CONTRIBUTING.md**
  - Code style guidelines
  - Branch strategy
  - PR process

- [ ] **Add code comments**
  - Docstrings for all functions
  - Inline comments for complex logic
  - Follow PEP 8 standards

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
