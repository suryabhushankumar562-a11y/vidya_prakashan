# 📚 Vidya Prakashan Mandir — Smart Online Bookstore
### Complete Django + DRF Setup Guide

---

## 🏗️ Project Structure

```
vidya_prakashan/
│
├── manage.py                      # Django entry point
├── requirements.txt               # Python dependencies
├── db.sqlite3                     # SQLite database (auto-created)
│
├── vidya_prakashan/               # Project configuration
│   ├── settings.py                # All Django settings
│   ├── urls.py                    # Root URL configuration
│   └── wsgi.py                    # WSGI entry point
│
├── accounts/                      # User authentication app
│   ├── models.py                  # UserProfile model
│   ├── views.py                   # Register, Login, Logout, Dashboard
│   ├── forms.py                   # RegisterForm, LoginForm
│   ├── urls.py                    # /accounts/* URL patterns
│   └── serializers.py             # DRF serializers
│
├── books/                         # Core book management app
│   ├── models.py                  # Book, Category, Review models
│   ├── views.py                   # Book list, detail, categories, PDF
│   ├── urls.py                    # /books/* URL patterns
│   ├── serializers.py             # DRF serializers
│   ├── context_processors.py      # Nav categories injector
│   └── management/commands/
│       └── seed_data.py           # Demo data command
│
├── cart/                          # Shopping cart app
│   ├── models.py                  # Cart, CartItem models
│   ├── views.py                   # Add, remove, update cart
│   ├── urls.py                    # /cart/* URL patterns
│   ├── serializers.py             # DRF serializers
│   └── context_processors.py     # Cart count injector
│
├── orders/                        # Order management app
│   ├── models.py                  # Order, OrderItem models
│   ├── views.py                   # Checkout, history, detail
│   ├── urls.py                    # /orders/* URL patterns
│   └── serializers.py             # DRF serializers
│
├── adminpanel/                    # Custom admin dashboard app
│   ├── views.py                   # All admin panel views
│   └── urls.py                    # /adminpanel/* URL patterns
│
├── api/                           # REST API app (DRF)
│   ├── views.py                   # All API endpoints
│   └── urls.py                    # /api/* URL patterns
│
├── templates/                     # All HTML templates
│   ├── base.html                  # Master layout (navbar, footer)
│   ├── home.html                  # Homepage
│   ├── about.html                 # About page
│   ├── accounts/                  # Auth templates
│   │   ├── register.html
│   │   ├── login.html
│   │   └── dashboard.html
│   ├── books/                     # Book templates
│   │   ├── book_list.html
│   │   ├── book_detail.html
│   │   ├── category_list.html
│   │   ├── category_books.html
│   │   └── pdf_viewer.html
│   ├── cart/
│   │   └── cart.html
│   ├── orders/
│   │   ├── checkout.html
│   │   ├── order_confirmation.html
│   │   ├── order_history.html
│   │   └── order_detail.html
│   └── adminpanel/
│       ├── base_admin.html
│       ├── dashboard.html
│       ├── book_list.html
│       ├── book_form.html
│       ├── category_list.html
│       ├── category_form.html
│       ├── user_list.html
│       ├── order_list.html
│       └── order_detail.html
│
├── static/
│   ├── css/main.css               # Complete custom stylesheet
│   └── js/main.js                 # Interactivity & AJAX
│
└── media/                         # Uploaded files (auto-created)
    ├── book_covers/
    └── book_pdfs/
```

---

## 🚀 Step-by-Step Setup

### Step 1 — Prerequisites
Make sure you have:
- Python 3.10+ installed: `python --version`
- pip installed: `pip --version`

### Step 2 — Create a Virtual Environment
```bash
# Create the environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run Database Migrations
```bash
# Create all database tables
python manage.py makemigrations accounts books cart orders
python manage.py migrate
```

### Step 5 — Seed Demo Data (Recommended)
```bash
# Creates 8 categories, 8 books, admin user, and demo user
python manage.py seed_data
```

This creates:
| User      | Password  | Role       |
|-----------|-----------|------------|
| `admin`   | `admin`| Superuser  |
| `apple_bhushan`| `Ravi@8917`| Normal user|

### Step 6 — Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 7 — Start the Development Server
```bash
python manage.py runserver
```

Open your browser and visit: **http://127.0.0.1:8000/**

---

## 🌐 URL Reference

| URL | Description |
|-----|-------------|
| `/` | Homepage with featured books & categories |
| `/about/` | About page |
| `/books/` | Full book catalog with search & filter |
| `/books/<slug>/` | Book detail page |
| `/books/<slug>/read/` | PDF viewer page |
| `/books/<slug>/pdf/` | Secure PDF file server |
| `/books/categories/` | All categories page |
| `/books/category/<slug>/` | Books by category |
| `/accounts/register/` | User registration |
| `/accounts/login/` | Login |
| `/accounts/logout/` | Logout |
| `/accounts/dashboard/` | User dashboard |
| `/cart/` | Shopping cart |
| `/cart/add/<id>/` | Add book to cart |
| `/cart/remove/<id>/` | Remove cart item |
| `/orders/checkout/` | Checkout page |
| `/orders/history/` | Order history |
| `/orders/<order#>/` | Order detail |
| `/adminpanel/` | Custom admin dashboard |
| `/adminpanel/books/` | Manage books |
| `/adminpanel/categories/` | Manage categories |
| `/adminpanel/orders/` | Manage orders |
| `/adminpanel/users/` | View users |
| `/django-admin/` | Django built-in admin |

---

## 🔌 REST API Reference

All endpoints are prefixed with `/api/`.

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | Register new user → returns JWT |
| `POST` | `/api/auth/login/` | Login → returns JWT access + refresh |
| `POST` | `/api/auth/token/refresh/` | Refresh JWT token |
| `GET`  | `/api/auth/me/` | Current user profile (auth required) |

#### Register Example
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "apple",
    "email": "apple@example.com",
    "password": "Apple@123",
    "confirm_password": "Apple@123"
  }'
```

#### Login Example
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Books

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/books/` | List all books (supports `?q=`, `?category=slug`, `?featured=1`) |
| `GET` | `/api/books/<slug>/` | Book detail |
| `GET` | `/api/books/<slug>/pdf-access/` | Check PDF access (auth required) |

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/categories/` | List all categories |
| `GET` | `/api/categories/<slug>/books/` | Books in a category |

### Cart (requires JWT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/cart/` | View cart |
| `POST` | `/api/cart/` | Add item `{book_id, quantity}` |
| `DELETE` | `/api/cart/<item_id>/` | Remove item |

#### Add to Cart Example
```bash
curl -X POST http://127.0.0.1:8000/api/cart/ \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1, "quantity": 1}'
```

### Orders (requires JWT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/orders/` | List user's orders |
| `POST` | `/api/orders/` | Place order from cart |
| `GET` | `/api/orders/<order_number>/` | Order detail |

---

## 🔐 Security Features

### PDF Security
- PDF files are stored in `media/book_pdfs/` — **not directly accessible via URL**
- Django's `FileResponse` serves the PDF only after authorization checks
- Non-logged-in users → 403 Forbidden
- Logged-in but not purchased → 403 Forbidden
- Admin/staff → always granted
- Purchased users → full access

### Authentication
- Django's built-in `AuthenticationMiddleware`
- `@login_required` decorator on all protected views
- `user_passes_test(is_staff)` for admin panel access
- JWT tokens for the REST API (via `djangorestframework-simplejwt`)
- CSRF protection on all POST forms

---

## ✏️ How to Add a Book (via Admin Panel)
1. Login at `/accounts/login/` with admin credentials
2. Go to `/adminpanel/books/add/`
3. Fill in title, author, select category, set price
4. Upload a cover image (JPEG/PNG recommended)
5. Upload the book PDF
6. Set "Active" and optionally "Featured"
7. Click "Add Book"

---

## 📦 How to Create a Category
1. Go to `/adminpanel/categories/add/`
2. Enter name (slug auto-generates)
3. Enter a Bootstrap Icons class name, e.g., `bi-calculator`
4. Click "Add Category"
5. Category immediately appears in navbar dropdown and category page

---

## 🎨 Customization

### Changing Colors
Edit `:root` variables in `static/css/main.css`:
```css
:root {
  --vp-primary:   #1a2744;   /* Deep navy — change to your brand color */
  --vp-secondary: #f5a623;   /* Saffron yellow — change to your accent */
  --vp-accent:    #e8572a;   /* Terracotta — change to your highlight */
}
```

### Changing the Site Name
Search and replace `Vidya Prakashan Mandir` in:
- `templates/base.html`
- `templates/adminpanel/base_admin.html`
- `vidya_prakashan/settings.py`

---

## 🛠️ Production Checklist
Before going live:
- [ ] Set `DEBUG = False` in `settings.py`
- [ ] Generate a strong `SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS = ['yourdomain.com']`
- [ ] Switch to PostgreSQL (update `DATABASES`)
- [ ] Run `python manage.py collectstatic`
- [ ] Set up Nginx to serve static & media files
- [ ] Use Gunicorn as the WSGI server
- [ ] Store secrets in environment variables (use `python-decouple`)
- [ ] Enable HTTPS

---

## 💡 Tech Stack Summary

| Component | Technology |
|-----------|-----------|
| Backend | Python + Django 4.2+ |
| REST API | Django REST Framework + SimpleJWT |
| Database | SQLite (dev) → PostgreSQL (prod) |
| Frontend | Bootstrap 5.3 + Bootstrap Icons |
| Fonts | Playfair Display + Inter (Google Fonts) |
| File Storage | Django media files (local / S3 in prod) |
| Auth | Django auth + JWT for API |

---

*Built with ❤️ for Vidya Prakashan Mandir — © 2024*
