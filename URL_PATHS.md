# FixNear - Complete URL Path Guide

## Application Overview
FixNear is a Django-based service provider platform where users can find local service providers for various services (electrician, plumber, carpenter, etc.).

---

## URL Routes Reference

### 1. **Home Page**
- **URL:** `/`
- **Route Name:** `home`
- **View Function:** `home()` in `services/views.py`
- **Template:** `index.html`
- **Description:** Landing page showing hero section, services grid, how it works, and featured providers
- **Access:** Public (No authentication required)
- **Template Tag:** `{% url 'home' %}`

---

### 2. **User Authentication Routes**

#### Login Page
- **URL:** `/login/`
- **Route Name:** `login`
- **View Function:** `login_view()` in `services/views.py`
- **Template:** `auth_login.html`
- **Method:** GET (display form) | POST (process login)
- **Description:** User login page with email/password form
- **Access:** Public, redirects to home if already authenticated
- **Form Fields:** 
  - `email` (required)
  - `password` (required)
  - `remember_me` (optional checkbox)
- **Features:**
  - Remember me functionality
  - Forgot password link (placeholder)
  - Social login buttons (Google, Facebook placeholders)
  - Link to signup page
  - Error/success messages
  - CSRF token protection
- **Template Tag:** `{% url 'login' %}`

#### Sign Up Page
- **URL:** `/signup/`
- **Route Name:** `signup`
- **View Function:** `signup_view()` in `services/views.py`
- **Template:** `auth_signup.html`
- **Method:** GET (display form) | POST (create user account)
- **Description:** User registration page with account type selection
- **Access:** Public, redirects to home if already authenticated
- **Form Fields:**
  - `first_name` (required)
  - `last_name` (required)
  - `email` (required, unique)
  - `phone` (required)
  - `city` (required)
  - `password` (required, min 6 characters)
  - `confirm_password` (required, must match password)
  - `account_type` (required, 'customer' or 'provider')
  - `agree_terms` (required checkbox)
- **Account Type Selection:**
  - **Customer:** Regular user looking for services
  - **Provider:** Service provider offering services
- **Features:**
  - Account type toggle with JavaScript
  - Client-side password validation
  - Client-side password matching validation
  - Auto-login after successful registration
  - Duplicate email detection
  - Error/success messages
  - Password strength checking (minimum 6 characters)
  - CSRF token protection
- **Post-Signup Redirect:**
  - If account_type = 'customer': Redirects to home
  - If account_type = 'provider': Redirects to provider registration form
- **Template Tag:** `{% url 'signup' %}`

#### Logout
- **URL:** `/logout/`
- **Route Name:** `logout`
- **View Function:** `logout_view()` in `services/views.py`
- **Method:** GET (logs out user and redirects)
- **Description:** Logs out the current user
- **Access:** Authenticated users only
- **Redirect After:** Home page (`/`)
- **Template Tag:** `{% url 'logout' %}`

---

### 3. **Service Provider Routes**

#### Providers List/Search
- **URL:** `/providers/`
- **Route Name:** `providers`
- **View Function:** `providers()` in `services/views.py`
- **Template:** `providers_list.html`
- **Method:** GET (display filtered list)
- **Description:** List all service providers with filtering options
- **Access:** Public (No authentication required)
- **Features:**
  - Dynamic filtering by service type
  - Dynamic filtering by location
  - Dynamic filtering by rating
  - Responsive grid layout (shows 6 providers per page)
  - Provider cards with avatar, name, service, rating
  - View Profile links to individual provider pages
- **Query Parameters:**
  - `service` (optional): Filter by service type (e.g., `?service=electrician`)
  - `location` (optional): Filter by location/city (e.g., `?location=warangal`)
  - `rating` (optional): Filter by minimum rating (e.g., `?rating=4.5`)
- **Template Tag:** `{% url 'providers' %}`

##### Example Filtered URLs:
```
/providers/                                    (all providers)
/providers/?service=electrician                (filter by service)
/providers/?location=warangal                  (filter by location)
/providers/?rating=4.5                         (filter by rating ≥ 4.5)
/providers/?service=electrician&location=warangal&rating=4.0  (multiple filters)
```

#### Individual Provider Profile
- **URL:** `/provider/<int:provider_id>/`
- **Route Name:** `provider_detail`
- **View Function:** `provider_detail()` in `services/views.py`
- **Template:** `provider_profile.html`
- **Method:** GET (display provider details)
- **Description:** Detailed view of a single service provider
- **Access:** Public (No authentication required)
- **URL Parameters:**
  - `provider_id` (required, integer): The unique ID of the provider
- **Features:**
  - Provider avatar and basic info
  - Rating and review count
  - Services offered with tags
  - Pricing information (hourly rate, call charge)
  - Availability status
  - Location and address
  - Work experience details
  - Customer reviews section (3 sample reviews)
  - Call Now and Message buttons
  - Verification badge
- **Template Tag:** `{% url 'provider_detail' provider_id %}`

##### Example URLs:
```
/provider/1/                (first provider)
/provider/2/                (second provider)
/provider/15/               (provider with ID 15)
```

#### Provider Registration Form
- **URL:** `/register/`
- **Route Name:** `add_provider`
- **View Function:** `add_provider()` in `services/views.py`
- **Template:** `provider_registration.html`
- **Method:** GET (display form) | POST (save provider profile)
- **Description:** Service provider registration/profile creation form
- **Access:** Authenticated users only (requires login)
- **Login Required:** Yes - redirects to `/login/` if not authenticated
- **Form Sections:**
  1. **Personal Information**
     - First Name
     - Last Name
     - Email
     - Phone
  2. **Service Information**
     - Service Category (dropdown)
     - Years of Experience
     - Services Offered (checkboxes)
  3. **Location Details**
     - City
     - State
     - Address
  4. **Pricing**
     - Hourly Rate
     - Call Charge
  5. **Documents**
     - Certificate/License Upload (drag-and-drop)
- **Features:**
  - File drag-and-drop upload
  - Form validation
  - Terms acceptance requirement
  - Cancel/Reset buttons
- **Form Fields Saved to ServiceProvider Model:**
  - `name` (combined first + last name)
  - `profession` (service category)
  - `phone`
  - `location` (city)
  - `email`
  - `experience_years`
  - `hourly_rate`
  - `bio`
- **Redirect After Successful Save:** `/providers/` (providers list)
- **Template Tag:** `{% url 'add_provider' %}`

---

### 4. **Admin Route**

#### Django Admin Panel
- **URL:** `/admin/`
- **Route Name:** N/A (built-in Django)
- **Description:** Django administration interface for managing data
- **Access:** Superuser/Admin only
- **Features:**
  - Manage ServiceProvider records
  - Manage User accounts
  - Manage Site configuration
- **Access Requirements:**
  - Create superuser: `python manage.py createsuperuser`
  - Login with admin credentials

---

## Complete URL Structure Summary

```
BASE_URL = http://127.0.0.1:8000 (development)
        = https://yourdomain.com (production)

✅ PUBLIC ROUTES (No login required):
   GET  /                                  → Homepage
   GET  /login/                            → Login page
   POST /login/                            → Process login
   GET  /signup/                           → Signup page
   POST /signup/                           → Create new account
   GET  /logout/                           → Logout user
   GET  /providers/                        → List all providers
   GET  /providers/?service=X              → Filter by service
   GET  /providers/?location=X             → Filter by location
   GET  /providers/?rating=X               → Filter by rating
   GET  /provider/<id>/                    → View provider profile
   GET  /admin/                            → Admin panel

🔒 PROTECTED ROUTES (Login required):
   GET  /register/                         → Provider registration form
   POST /register/                         → Save provider profile
```

---

## Django Template URL Tags

### Usage in Templates
Instead of hardcoding URLs, use Django's `{% url %}` template tag:

```html
<!-- Navigation Links -->
<a href="{% url 'home' %}">Home</a>
<a href="{% url 'login' %}">Login</a>
<a href="{% url 'signup' %}">Sign Up</a>
<a href="{% url 'logout' %}">Logout</a>
<a href="{% url 'providers' %}">Find Services</a>
<a href="{% url 'add_provider' %}">Become Provider</a>

<!-- Provider Detail Link (with parameter) -->
<a href="{% url 'provider_detail' provider.id %}">View Profile</a>

<!-- Form Submission -->
<form method="POST" action="{% url 'login' %}">
    {% csrf_token %}
    ...
</form>
```

---

## Authentication System Details

### Login Credentials Flow
1. User opens `/login/`
2. Enters email and password
3. System:
   - Looks up User by email
   - Authenticates password
   - Creates session
   - Sets `user.is_authenticated = True`
4. Redirects to home with success message

### Signup New Account Flow
1. User opens `/signup/`
2. Selects account type (Customer/Provider)
3. Fills form with:
   - Name, email, phone, city
   - Password (minimum 6 characters)
   - Confirms password match
4. System:
   - Validates passwords match
   - Checks email not already registered
   - Creates User account
   - Creates ServiceProvider profile (if provider type)
   - Auto-logs in the user
   - Creates session
5. Redirects:
   - Customers → Home page
   - Providers → Provider registration form

### Session Management
- Session duration: Default Django settings (2 weeks)
- Session storage: Database (`django_session` table)
- Session cookie: `sessionid`
- CSRF token: Required for all POST requests

---

## Status Codes & Error Handling

### Successful Responses
- **200 OK:** Page loaded successfully
- **302 Found:** Redirect (after form submission)
- **304 Not Modified:** Cached content

### Client Errors
- **400 Bad Request:** Invalid form data
- **401 Unauthorized:** Not authenticated (for protected routes)
- **403 Forbidden:** User doesn't have permission
- **404 Not Found:** Page/provider doesn't exist
  - `/provider/9999/` → Returns 404 if provider doesn't exist

### Server Errors
- **500 Internal Server Error:** Server-side exception

---

## Development vs Production Note

### Development Server
```bash
cd c:\Users\Baigan\Documents\EY_4.O_Team_4\EY_4.O_Team_4\EY_4.O_Team_4\
myenv\Scripts\Activate.ps1
python manage.py runserver 0.0.0.0:8000
# Access at: http://127.0.0.1:8000/
```

### Production Deployment
- Use production WSGI server (Gunicorn, uWSGI)
- Change `DEBUG = False` in settings.py
- Update `ALLOWED_HOSTS` with domain
- Configure static files with STATIC_ROOT
- Set up HTTPS/SSL certificate
- Update database to PostgreSQL (recommended)

---

## File Structure Reference

```
services/
├── models.py          (ServiceProvider model with 15+ fields)
├── views.py           (Home, Login, Signup, Logout, Providers, Details, Register)
├── urls.py            (URL routing configuration)
└── forms.py           (Form definitions - if needed)

templates/
├── index.html                    (Homepage)
├── auth_login.html               (Login page)
├── auth_signup.html              (Signup page)
├── header_new.html               (Navigation bar)
├── footer_new.html               (Footer)
├── providers_list.html           (Provider search/listing)
├── provider_profile.html         (Provider detail)
└── provider_registration.html    (Provider registration form)

static/
├── style_new.css                 (Main stylesheet - 987 lines)
└── images/
    ├── service-icons/            (12 SVG service icons)
    └── avatars/                  (3 sample avatar SVGs)

fixnear/
├── settings.py        (Django configuration)
├── urls.py           (Main URL router)
├── wsgi.py           (WSGI application)
└── asgi.py           (ASGI application)

manage.py             (Django management script)
db.sqlite3            (SQLite database)
```

---

## Quick Reference Table

| Feature | Route | Method | Auth Required | Description |
|---------|-------|--------|---------------|-------------|
| Homepage | `/` | GET | No | Landing page |
| Login | `/login/` | GET/POST | No | User login |
| Signup | `/signup/` | GET/POST | No | New account |
| Logout | `/logout/` | GET | Yes | Logout user |
| Providers List | `/providers/` | GET | No | Search providers |
| Provider Detail | `/provider/<id>/` | GET | No | View profile |
| Register Provider | `/register/` | GET/POST | Yes | Create provider |
| Admin | `/admin/` | GET/POST | Yes (Admin) | Manage data |

---

## Notes for Developers

1. **Always use `{% url 'route_name' %}` in templates** to avoid hardcoded URL breakage
2. **CSRF tokens required** for all POST requests (auto-included with `{% csrf_token %}`)
3. **Protected routes** automatically redirect to login if user not authenticated
4. **Session management** handled by Django automatically
5. **Database connections** use SQLite in development, configure PostgreSQL for production
6. **Static files** served in development mode, use `collectstatic` for production
7. **Messages framework** used for success/error notifications
8. **Responsive design** tested on 480px, 768px, and 1024px breakpoints

---

**Last Updated:** February 24, 2026
**Django Version:** 6.0.2
**Python Version:** 3.x
**Development Status:** ✅ Running
**Server:** http://127.0.0.1:8000/
