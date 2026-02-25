# FixNear - Quick Start & Feature Guide

**Version:** 2.0 Enhanced  
**Last Updated:** February 25, 2026

---

## 🚀 Quick Start

### Start the Server
```powershell
cd c:\Users\Baigan\Documents\EY_4.O_Team_4\EY_4.O_Team_4\EY_4.O_Team_4
myenv\Scripts\Activate.ps1
python manage.py runserver 0.0.0.0:8000
```

### Access the App
- **Home:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/ (requires superuser)

---

## 👥 User Roles

### Customers
- Browse service providers
- Search and filter services
- Create bookings
- Track booking status
- Cancel pending bookings
- View booking history
- Manage profile and settings

### Providers
- Manage service offerings
- View incoming booking requests
- Approve/reject/complete bookings
- Track acceptance statistics
- Set availability status
- Manage pricing and rates
- View analytics dashboard

---

## 🔑 Key Features

### 1. Real-Time Booking Status
- Automatic polling every 5 seconds
- Live status updates without page refresh
- Visual status badges (pending, approved, completed, rejected, cancelled)

### 2. Smart Provider Dashboard
- View all bookings with status filter
- See completion rate percentage
- Accept/reject/complete bookings one-click
- Track total jobs and ratings

### 3. Smart Customer Dashboard
- overview of all bookings
- Success rate calculation
- Quick access to all features
- Real-time status updates

### 4. Advanced Search & Filtering
- Search providers by profession/bio
- Filter by location (city)
- Filter by minimum rating
- Sort by rating or experience
- Pagination support

### 5. Booking Management
- Create detailed booking requests
- Add custom notes
- Cancel pending/approved bookings
- View full booking history
- Automatic email notification ready

---

## 📊 Dashboard Metrics

### Provider Dashboard Shows
- 📋 Pending Bookings Count
- ✅ Approved Bookings Count
- 🏁 Completed Bookings Count
- ❌ Rejected Bookings Count
- ⭐ Provider Rating (0-5)
- 📊 Completion Rate (%)

### Customer Dashboard Shows
- 📅 Total Bookings Count
- ✅ Completed Bookings Count
- ⏳ Pending Bookings Count
- ✔️ Approved Bookings Count
- ❌ Rejected Bookings Count
- 📊 Success Rate (%)

---

## 🔌 API Endpoints

### Booking Status Poll (Real-time)
```
GET /bookings/status/
Response: { "bookings": { "1": "approved", "2": "pending", ... } }
```

### Get All Customer Bookings
```
GET /api/bookings/
Parameters:
  - status: pending|approved|completed|rejected|cancelled
  - provider: provider_id
  - date_from: YYYY-MM-DD
  - date_to: YYYY-MM-DD
  - sort: -created_at|created_at|-booking_date|booking_date
  - page: integer
  - per_page: integer (default: 10)
```

### Get Provider Bookings with Analytics
```
GET /api/provider-bookings/
Parameters:
  - status: pending|approved|completed|rejected|cancelled
  - date_from: YYYY-MM-DD
  - date_to: YYYY-MM-DD
  - page: integer
  - per_page: integer

Response includes:
- Provider details (name, profession, rating)
- Statistics (total, pending, approved, completed, rejected, cancelled, completion_rate)
- List of bookings with customer details
```

### Cancel Booking
```
POST /booking/<booking_id>/cancel/
Response: Redirect to /my_bookings/ with success message
Note: Only pending and approved bookings can be cancelled
```

### Update Booking Status (Provider Only)
```
POST /booking/<booking_id>/update/<status>/
Statuses: approved|rejected|completed|cancelled
Note: Can only transition from pending to approved/rejected
      From approved to completed
```

---

## 🔐 Login Credentials (Test Data)

### Test Customer
- **Email:** test_customer@example.com
- **Password:** password123 (or set your own)
- **Role:** Customer

### Test Provider
- **Email:** test_provider@example.com
- **Password:** password123
- **Role:** Provider

### Create Your Own
- Visit `/signup/`
- Choose role (Customer or Provider)
- Email must be unique
- Password minimum 6 characters

---

## 📱 Responsive Design

Works perfectly on:
- 📱 Mobile (320px and up)
- 📱 Tablet (768px)
- 💻 Desktop (1024px+)

All features fully responsive with touch-friendly buttons.

---

## 🗂️ File Structure

```
FixNear/
├── manage.py                    # Django management
├── db.sqlite3                   # SQLite database
├── test_features.py            # Comprehensive tests
├── fixnear/                     # Main project
│   ├── settings.py             # Configuration
│   ├── urls.py                 # Root URL routes
│   ├── wsgi.py                 # WSGI app
│   └── asgi.py                 # ASGI app
├── services/                    # Main app
│   ├── models.py               # Database models
│   ├── views.py                # View logic
│   ├── urls.py                 # App routes
│   ├── signals.py              # Event handlers (NEW)
│   └── admin.py                # Admin config
├── templates/                   # HTML templates
│   ├── index.html              # Homepage
│   ├── auth_login.html         # Login page
│   ├── auth_signup.html        # Signup page
│   ├── provider_dashboard.html # Provider panel
│   ├── customer_dashboard.html # Customer panel
│   ├── my_bookings.html        # Booking list
│   └── ... (13 more templates)
├── static/                     # CSS, images
│   ├── style_new.css          # Main stylesheet
│   └── images/                # SVG icons
└── staticfiles/               # Collected static files
```

---

## 🧪 Run Tests

### Comprehensive Feature Test
```powershell
python test_features.py
```

### Django System Check
```powershell
python manage.py check
```

### Load Test Data
```powershell
python manage.py create_test_data
```

---

## ⚙️ Configuration

### Database
- Type: SQLite
- File: `db.sqlite3`
- Migrations: Already applied

### Static Files
```powershell
python manage.py collectstatic --noinput
```

### Create Admin User
```powershell
python manage.py createsuperuser
# Then access /admin/
```

---

## 🐛 Troubleshooting

### "Page not found" (404)
- Check URL in address bar
- Verify route exists in services/urls.py
- Run `python manage.py check`

### "Forbidden" (403)
- Wrong HTTP method (POST vs GET)
- Missing CSRF token
- Check view permissions

### Template not found
- Verify template file exists in templates/
- Check template name in render() call
- File names are case-sensitive

### Database errors
- Run migrations: `python manage.py migrate`
- Check if db.sqlite3 exists
- Reset database: `python manage.py flush` (deletes data!)

### Server won't start
- Check port 8000 is available
- Run `python manage.py check`
- Check for syntax errors in views.py

---

## 📈 Performance Tips

1. **Enable DEBUG=False in production**
   - Settings.py line 30

2. **Use HTTPS in production**
   - Set SECURE_SSL_REDIRECT = True
   - Set SECURE_HSTS_SECONDS = 31536000

3. **Set proper ALLOWED_HOSTS**
   - For production: `['yourdomain.com', 'www.yourdomain.com']`

4. **Use a production WSGI server**
   - Gunicorn, uWSGI, or similar

5. **Enable caching**
   - Redis or Memcached for sessions

---

## 🔄 Workflow Examples

### Book a Service (Customer)
1. Sign up or log in
2. Click "Find Services"
3. Search or filter providers
4. Click "Book Now" on provider card
5. Fill booking form
6. Submit
7. View booking in "My Bookings"
8. Watch status change in real-time

### Approve a Booking (Provider)
1. Sign up or log in as provider
2. Go to "Provider Dashboard"
3. See pending booking requests
4. Click "✓ Approve" button
5. Confirmation modal appears
6. Customer sees status update instantly

### Track Completion (Provider)
1. Booking is "Approved"
2. After service completion
3. Click "✓ Mark Complete"
4. Booking moves to "Completed" status
5. Statistics updated automatically

---

## 📞 Quick Feature Reference

| Feature | Customer | Provider |
|---------|----------|----------|
| Register | ✅ | ✅ |
| Login | ✅ | ✅ |
| Browse Providers | ✅ | ✗ |
| Search Services | ✅ | ✗ |
| Create Booking | ✅ | ✗ |
| Cancel Booking | ✅ | ✗ |
| View Bookings | ✅ | ✅ |
| Approve Booking | ✗ | ✅ |
| Complete Booking | ✗ | ✅ |
| Manage Services | ✗ | ✅ |
| View Dashboard | ✅ | ✅ |
| View Profile | ✅ | ✅ |
| Edit Settings | ✅ | ✅ |

---

## 🎯 URL Reference

### Public Pages
- `/` - Homepage
- `/login/` - Login page
- `/signup/` - Registration
- `/providers/` - All providers
- `/provider/<id>/` - Provider detail

### Customer Routes
- `/customer/dashboard/` - Customer dashboard
- `/customer/find-services/` - Find services
- `/customer/my-bookings/` - My bookings
- `/customer/profile/` - My profile
- `/customer/settings/` - My settings

### Provider Routes
- `/provider/dashboard/` - Provider dashboard
- `/provider/my-requests/` - Booking requests
- `/provider/my-services/` - Manage services
- `/provider/profile/` - My profile
- `/provider/settings/` - My settings

### Booking Routes
- `/booking/<provider_id>/` - Create booking form
- `/booking/<id>/update/<status>/` - Update status
- `/booking/<id>/cancel/` - Cancel booking

### API Routes
- `/bookings/status/` - Real-time status poll
- `/api/bookings/` - Customer bookings API
- `/api/provider-bookings/` - Provider bookings API

---

**✅ All Features Ready to Use!**

For detailed technical documentation, see:
- IMPLEMENTATION_ENHANCEMENT_REPORT.md
- IMPLEMENTATION_COMPLETE.md
- AUTHENTICATION_SUMMARY.md
- URL_PATHS.md
