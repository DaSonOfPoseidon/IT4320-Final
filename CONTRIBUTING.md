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

## Code Formatting & Linting

We use **Black** for automatic code formatting and **Ruff** for fast linting.

### Run Before Committing

```bash
# Format code with Black (100 char line length)
black --line-length 100 .

# Lint code with Ruff
ruff check .

# Auto-fix linting issues
ruff check --fix .
```

### IDE Integration

**VS Code**: Install extensions:
- Black Formatter
- Ruff

Add to `.vscode/settings.json`:
```json
{
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "python.linting.ruffEnabled": true
}
```

**PyCharm**: Configure Black and Ruff in Settings → Tools → External Tools

### Pre-commit Workflow

1. Write code
2. Run `black --line-length 100 .`
3. Run `ruff check --fix .`
4. Fix any remaining issues
5. Commit changes

## Testing Checklist

Before submitting PR:

- [ ] Code formatted with Black
- [ ] Ruff linting passes with no errors
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
