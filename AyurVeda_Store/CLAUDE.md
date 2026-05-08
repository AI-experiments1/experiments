# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
python run.py          # starts Flask dev server at http://127.0.0.1:5000
```

The database (`instance/ayurveda_store.db`) and seed data are created automatically on first run via `db.create_all()` + `seed_data()` inside the app factory.

**Default admin credentials:** `admin@ayurvedastore.com` / `admin123`

## Dependencies

```bash
pip install -r requirements.txt
```

Requires **Pillow >= 11.0.0** (not 10.x) when running on Python 3.14 — 10.x has no prebuilt wheel for 3.14 and fails to compile from source on Windows.

## Architecture

Single Flask application using the **app factory pattern** (`app/__init__.py` → `create_app()`). Five Blueprints are registered with these URL prefixes:

| Blueprint | Prefix | File |
|-----------|--------|------|
| `main` | `/` | `routes/main.py` |
| `auth` | `/auth` | `routes/auth.py` |
| `products` | `/products` | `routes/products.py` |
| `cart` | `/cart` | `routes/cart.py` |
| `admin` | `/admin` | `routes/admin.py` |

**Admin access** is gated by a custom `@admin_required` decorator (in `routes/admin.py`) that checks `current_user.is_admin`. All cart and auth routes use Flask-Login's `@login_required`.

## Data Model

Six SQLAlchemy models in `app/models.py`:

- **User** — `is_admin` flag for admin access; `cart_items` and `orders` relationships
- **Category** — identified by `slug` (`'ayurvedic'` / `'agricultural'`); used in URL query params
- **Product** — `is_featured` drives homepage display; `is_active` gates customer visibility; `discount_percent` is a computed property
- **CartItem** — join between User and Product; `subtotal` is a computed property
- **Order** — status lifecycle: `Pending → Confirmed → Shipped → Delivered / Cancelled`; stock is decremented at checkout
- **OrderItem** — snapshots `price` at time of purchase (not a live FK to current price)

## Key Patterns

**Seeding:** `app/seed.py:seed_data()` is called on every app start but short-circuits if any `Category` row exists. To reset data, delete `instance/ayurveda_store.db`.

**Forms:** All forms are WTForms classes in `app/forms.py`. CSRF is handled automatically by Flask-WTF — every POST form needs `{{ form.hidden_tag() }}` in the template.

**Free delivery threshold:** ₹999. This logic lives only in templates (`cart.html`, `checkout.html`) — not enforced in the backend `Order.total`.

**Category filtering** in `products/list_products` uses `Category.slug` (not `id`) as the query param: `?category=ayurvedic`.

## Configuration

Environment variables are loaded from `.env` via `python-dotenv`:

```
SECRET_KEY=...
DATABASE_URL=sqlite:///ayurveda_store.db
```

`DATABASE_URL` is passed directly to `SQLALCHEMY_DATABASE_URI`, so switching to PostgreSQL requires only changing that value.

## Tests

```bash
pytest                  # run all tests
pytest tests/test_models.py          # single file
pytest tests/test_cart.py::test_add_to_cart  # single test
pytest -v               # verbose output
```

Tests live in `tests/`. Each test function gets a **fresh in-memory SQLite database** (function-scoped `app` fixture with `StaticPool`) so there is no state leakage between tests.

**Fixtures** (defined in `tests/conftest.py`):
- `client` — unauthenticated test client
- `auth_client` — pre-logged-in as `user@test.com` / `testpass123`
- `admin_client` — pre-logged-in as `admin@test.com` / `adminpass123`

**Key test config differences from production:**
- `WTF_CSRF_ENABLED=False` — form submissions don't need a CSRF token
- `TESTING=True` — skips `seed_data()` in the app factory; tests seed their own minimal data via `conftest._seed()`
- `StaticPool` — all DB sessions share the same in-memory connection, so data written inside a request is visible in `with app.app_context():` blocks in the same test

When adding new routes, add corresponding tests. When adding new models or computed properties, add unit tests in `test_models.py` first.