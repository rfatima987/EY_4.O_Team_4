# FixNear Platform - Complete Design & Architecture

## 1. Platform Overview

**FixNear** is a local service booking platform with two distinct user roles:
- **Customers**: Search, find, and book services from providers
- **Service Providers**: Manage bookings, services, and customer interactions

---

## 2. URL Structure (Organized by Role)

### Authentication Routes
```
/                          → Home Page
/login/                    → Login
/logout/                   → Logout
/signup/                   → Registration (with role selection)
```

### Main Dashboard (Smart Routing)
```
/dashboard/                → Redirect to customer_dashboard or provider_dashboard based on user role
```

### Customer Routes
```
/customer/dashboard/       → Customer Dashboard (overview, stats, quick actions)
/customer/find-services/   → Find & Search Services (with filters)
/customer/my-bookings/     → View My Bookings (real-time status updates)
/customer/profile/         → Edit Personal Profile
/customer/settings/        → Account Settings & Preferences
```

### Provider Routes
```
/provider/dashboard/       → Provider Dashboard (overview, stats)
/provider/my-requests/     → Manage Booking Requests (pending)
/provider/my-services/     → Manage Services Offered
/provider/profile/         → Edit Professional Profile
/provider/settings/        → Account & Availability Settings
/provider/register/        → Registration Form for Providers
```

### Service Operations
```
/providers/                → List All Providers
/provider/<id>/            → View Provider Public Profile
/booking/<provider_id>/    → Create Booking Form
/booking/<id>/update/<status>/  → Update Booking Status (POST only)
/bookings/status/          → JSON API for Real-time Status Updates
```

---

## 3. Navigation System - Role-Based Header

### Header Features:
- **Smart Detection**: Automatically detects user role (Customer vs Provider)
- **Responsive Design**: Mobile-friendly hamburger menu
- **Dynamic Menus**: Different navigation options based on role

**Customer Navigation:**
- 🏠 Dashboard
- 🔍 Find Services
- 📅 My Bookings
- 👤 Profile
- ⚙️ Settings
- 🚪 Logout

**Provider Navigation:**
- 📊 Dashboard
- 📬 My Requests
- 🛠️ Services
- 👤 Profile
- ⚙️ Settings
- 🚪 Logout

---

## 4. Customer Interface

### 4.1 Customer Dashboard (`/customer/dashboard/`)
**Purpose**: Overview of bookings and quick access to services

**Features:**
- Welcome greeting with user's name
- Statistics cards:
  - Total bookings count
  - Completed bookings
  - Pending bookings
- Quick action buttons:
  - Find Services
  - My Bookings
  - Profile
  - Browse All Providers
- Recent bookings list with status badges
- Empty state message if no bookings

### 4.2 Find Services (`/customer/find-services/`)
**Purpose**: Search and discover service providers

**Features:**
- Advanced search filters:
  - Text search (service name, provider name)
  - Profession filter
  - Location filter
  - Minimum rating filter
- Provider cards displaying:
  - Provider name & profession
  - Avatar/profile picture
  - Star rating (visual stars)
  - Years of experience
  - Hourly rate
  - Service description preview
  - View Profile button
  - Book Now button
- Grid layout (3 columns on desktop, 1 on mobile)
- Empty state when no results found

### 4.3 My Bookings (`/customer/my-bookings/`)
**Purpose**: View and track all bookings with real-time updates

**Features:**
- Side-by-side booking cards (2-column grid)
- Per booking card info:
  - Booking ID
  - Provider name
  - Service requested
  - Date & time
  - Booking status (with color-coded badge)
  - Customer details (phone, address, contact)
  - Notes
- Real-time status updates via polling (5-second intervals)
- Status badges:
  - Pending (yellow)
  - Approved (green)
  - Rejected (red)
  - Completed (blue)
  - Cancelled (gray)

### 4.4 Customer Profile (`/customer/profile/`)
**Purpose**: View and edit personal information

**Features:**
- Profile header with avatar, name, email
- Edit form:
  - First Name
  - Last Name
  - Email (display only)
- Statistics:
  - Total bookings
  - Completed bookings
  - Member since year
- Save/Cancel buttons

### 4.5 Customer Settings (`/customer/settings/`)
**Purpose**: Account management and preferences

**Sections:**
1. **Account Settings**
   - Update first name, last name
   - Email display (read-only)

2. **Password Settings**
   - Change password securely
   - Current password verification
   - New password confirmation

3. **Notification Preferences**
   - Email notifications:
     - Booking status updates
     - Provider messages
     - Weekly newsletter
     - Special promotions

4. **Privacy & Security**
   - Profile visibility to providers
   - Allow provider contact
   - Account deletion option

5. **Help & Support**
   - FAQs
   - Contact information

---

## 5. Provider Interface

### 5.1 Provider Dashboard (`/provider/dashboard/`)
**Purpose**: Overview of business and pending requests

**Features:**
- Provider name and profession header
- Statistics cards:
  - Pending booking requests
  - Approved bookings
  - Rejected bookings
  - Total jobs completed
- Quick actions:
  - View My Requests
  - Manage Services
  - Edit Profile
  - View Analytics
- Recent activity feed
- Average rating display

### 5.2 My Requests (`/provider/my-requests/`)
**Purpose**: Manage incoming booking requests from customers

**Features:**
- Pending requests displayed as cards
- Per request card info:
  - Customer name
  - Service requested
  - Date & time
  - Location/address
  - Phone number
  - Special notes/requirements
- Action buttons:
  - ✓ Approve (marks as 'approved')
  - ✗ Reject (marks as 'rejected')
- Confirmation dialogs before accepting/rejecting
- Empty state message when all requests handled
- POST-protected actions with CSRF tokens

### 5.3 My Services (`/provider/my-services/`)
**Purpose**: Manage and update services offered

**Features:**
- Edit service information form:
  - Service Type (e.g., Plumbing)
  - Profession (e.g., Plumber)
  - Hourly rate ($)
  - Service call charge ($)
  - Service description/bio (textarea)
- Tip/info box with guidelines
- Save/Cancel buttons

### 5.4 Provider Profile (`/provider/profile/`)
**Purpose**: Manage professional information and profile

**Features:**
- Header with avatar and key info:
  - Name
  - Profession
  - Rating
  - Total jobs completed
  - Years of experience
- Statistics cards:
  - Total bookings
  - Completed jobs
  - Average rating
- Editable form:
  - Full name
  - Profession
  - Years of experience
  - Phone number
  - City & State
  - Full address
  - Professional bio
- Save/Cancel buttons

### 5.5 Provider Settings (`/provider/settings/`)
**Purpose**: Account and availability management

**Sections:**
1. **Account Settings**
   - Edit first name, last name
   - Email (read-only)

2. **Availability Settings**
   - Available / Unavailable toggle
   - Working hours display
   - Status impacts booking availability

3. **Notification Preferences**
   - Email notifications for new requests
   - Booking status updates
   - Customer messages
   - SMS notifications
   - Weekly performance reports

4. **Privacy & Security**
   - Profile visibility toggle
   - Allow customer ratings/reviews
   - Phone number sharing settings

5. **Help & Support**
   - Provider-specific FAQs
   - Contact support information

---

## 6. Data Models

### User Model (Django Built-in)
```python
- user_id (PK)
- username
- email
- first_name
- last_name
- password (hashed)
- is_authenticated
- date_joined
```

### ServiceProvider Model
```python
- id (PK)
- user (OneToOneField to User, nullable for auto-linking)
- name
- email
- phone
- profession
- bio/description
- location/city/state/address
- service_type
- experience_years
- hourly_rate
- call_charge
- rating
- verified (boolean)
- availability (available/not_available)
- total_jobs
- created_at
```

### Booking Model
```python
- id (PK)
- provider (FK to ServiceProvider)
- customer_user (FK to User)
- customer_name
- customer_phone
- customer_email
- customer_address
- service
- booking_date
- booking_time
- notes
- status (pending/approved/rejected/completed/cancelled)
- created_at
- updated_at
```

---

## 7. Key Features & Functionality

### 7.1 Role-Based Access Control
- Smart dashboard routing based on whether user is a provider
- Auto-linking provider profiles by email
- Separate navigation menus for each role
- @login_required decorators on protected views

### 7.2 Real-Time Status Updates
- JavaScript polling (5-second intervals) on customer booking view
- JSON endpoint `/bookings/status/` returns booking statuses
- Status badges update dynamically without page refresh
- Color-coded status indicators

### 7.3 CSRF Protection
- All POST actions protected with `{% csrf_token %}`
- Explicit hidden input fields in forms
- POST-only views for state-changing operations

### 7.4 Responsive Design
- Mobile-first approach
- Grid layouts adapt from 2 columns to 1 on mobile
- Hamburger menu on mobile (header)
- Touch-friendly buttons and forms

### 7.5 Search & Filtering
- Text search across provider names and services
- Location-based filtering
- Rating-based filtering
- Profession filtering

---

## 8. Navigation Flow

### Customer Journey
1. User visits homepage
2. Clicks "Sign Up" → Chooses "Customer" role → Creates account
3. Automatically redirected to customer dashboard
4. Clicks "Find Services"
5. Searches and filters providers
6. Clicks "Book Now" on chosen provider
7. Fills booking form
8. Booking created with "Pending" status
9. Views in "My Bookings"
10. Watches real-time status updates as provider approves
11. Final status updates to "Approved" or "Rejected"

### Provider Journey
1. User visits homepage
2. Clicks "Sign Up" → Chooses "Provider" role → Creates account
3. Completes provider registration
4. Automatically redirected to provider dashboard
5. Clicks "My Requests" to see pending bookings
6. Reviews customer details
7. Clicks "Approve" or "Reject"
8. Status updates immediately for customer (via polling)
9. Can manage availability and services anytime

---

## 9. Technical Implementation

### Backend (Django)
- Views: 16 function-based views handling all routes
- Models: 3 models (User, ServiceProvider, Booking)
- Authentication: Django built-in auth system
- CSRF Protection: Middleware + template tags
- JSON API: `/bookings/status/` endpoint for polling

### Frontend
- Template System: Django templates
- Styling: custom CSS + Poppins font
- JavaScript: Polling script, section toggles, mobile menu
- Responsive: CSS Grid, Media queries, Flexbox

### Key Templates
- `header_role_based.html` - Smart navigation
- `customer_dashboard.html`
- `find_services.html`
- `customer_profile.html`
- `customer_settings.html`
- `provider_requests.html`
- `provider_services.html`
- `provider_profile.html`
- `provider_settings.html`
- `my_bookings.html` (existing - enhanced)

---

## 10. Installation & Setup

1. **Create User Accounts**
   ```
   Navigate to /signup/
   Choose role: "Customer" or "Provider"
   Complete registration
   ```

2. **Set Availability (Provider)**
   ```
   Go to /provider/settings/
   Toggle between "Available" and "Unavailable"
   ```

3. **Create Bookings (Customer)**
   ```
   Go to /customer/find-services/
   Search for providers
   Click "Book Now"
   Fill booking details
   Submit booking
   ```

4. **Manage Requests (Provider)**
   ```
   Go to /provider/my-requests/
   Review customer details
   Click "Approve" or "Reject"
   Status updates in real-time for customer
   ```

---

## 11. Future Enhancements

- Payment integration (Stripe/PayPal)
- Review & rating system
- Messaging/chat system
- Provider analytics dashboard
- Email notifications
- SMS alerts
- Password reset via email
- Social login (Google, Facebook)
- Advanced analytics for providers
- Customer support ticket system
- Admin dashboard

---

**Platform Status**: ✅ Role-based navigation and interfaces fully implemented
**Last Updated**: February 24, 2026
