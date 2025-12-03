# Contributing Guide

## Setup

```bash
python -m venv venv
venv\Scripts\activate  # Windows | source venv/bin/activate (Mac/Linux)
pip install -r requirements.txt
python app.py
```

## Workflow

1. Create branch: `git checkout -b feature/your-feature-name`
2. Make changes and test
3. Commit with descriptive message
4. Push: `git push origin feature/your-feature-name`
5. Create pull request for review

**Branch Types**: `feature/<name>`, `bugfix/<name>`, `docs/<name>`

## Code Standards

- PEP 8: 4 spaces, 100 char lines, descriptive names
- Add docstrings to all functions
- Use # for comments
- Update docs when adding features

```python
# Good
def calculate_seat_price(row):
    """Calculate price based on seat row."""
    if row <= 4:
        return 30.00
    elif row <= 8:
        return 20.00
    else:
        return 10.00
```

## Testing Checklist

Before submitting PR:

- [ ] All routes accessible
- [ ] Forms validate correctly
- [ ] Database operations work (create, read, delete)
- [ ] Admin auth works
- [ ] Seat availability checked
- [ ] E-ticket generation unique
- [ ] Total sales accurate

**Key Scenarios**: Reservation flow, admin dashboard, error handling (duplicate seats, invalid input, bad login)

## Commit Messages

Format: `<type>: <subject>`

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

```
feat: add seat reservation form with validation
fix: prevent duplicate seat reservations
docs: update README with pricing structure
```

## Pull Requests

1. Follow code style
2. Test thoroughly
3. Update docs
4. Keep branch current with `main`
5. Get one team review
6. Merge and delete branch

## Common Tasks

**Add Route**:
```python
@app.route('/route', methods=['GET', 'POST'])
def function():
    """Description"""
    pass
```

**Templates**: Extend `base.html`, use Bootstrap 5, link to home

**Schema Changes**: Update `schema.sql` + SQLAlchemy models in `app.py`
