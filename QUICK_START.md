# FixNear - Quick Start Guide

## 🚀 Start the Application (30 seconds)

```powershell
# Step 1: Navigate to project directory
cd c:\Users\Baigan\Documents\EY_4.O_Team_4\EY_4.O_Team_4\EY_4.O_Team_4\

# Step 2: Activate virtual environment
myenv\Scripts\Activate.ps1

# Step 3: Run development server
python manage.py runserver 0.0.0.0:8000
```

**Server will be available at:** `http://127.0.0.1:8000/`

---

## 📍 Important URLs

### For Customers
- **Homepage:** http://127.0.0.1:8000/
- **Find Services:** http://127.0.0.1:8000/providers/
- **Sign Up:** http://127.0.0.1:8000/signup/
- **Login:** http://127.0.0.1:8000/login/

### For Service Providers
- **Become Provider:** http://127.0.0.1:8000/register/ (requires login)
- **View Providers:** http://127.0.0.1:8000/providers/

### Admin
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 🧪 Test User Account

**To test without creating new account:**

1. Go to `/admin/`
2. Log in with superuser credentials (if created)
3. Or create new user:

```powershell
python manage.py createsuperuser
# Follow prompts to create admin account
```

**Test as new user:**
1. Go to `/signup/`
2. Fill in form and create account
3. Will auto-login
4. Explore the platform

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `URL_PATHS.md` | Complete URL routing reference |
| `AUTHENTICATION_SUMMARY.md` | User auth system details |
| `IMPLEMENTATION_COMPLETE.md` | Full project status |
| `FIXNEAR_README.md` | Project overview |

---

## ✅ Quick Verification Checklist

After starting server, verify:

- [ ] Homepage loads at `/`
- [ ] Can view providers at `/providers/`
- [ ] Can search by service, location, rating
- [ ] Can view provider detail pages
- [ ] Can click signup (`/signup/`)
- [ ] Can create new user account
- [ ] Can login (`/login/`)
- [ ] Can logout
- [ ] Can register as provider (`/register/`)
- [ ] Header shows correct buttons (login/signup or dropdown)

---

## 🔧 Common Commands

```bash
# Run development server
python manage.py runserver 0.0.0.0:8000

# Create new user (admin)
python manage.py createsuperuser

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Open Django shell
python manage.py shell

# Run tests
python manage.py test

# Database reset (WARNING: deletes all data)
python manage.py flush
```

---

## 🚨 If Something Goes Wrong

**Module not found error?**
```powershell
# Make sure venv is activated
myenv\Scripts\Activate.ps1
```

**Port 8000 already in use?**
```powershell
python manage.py runserver 0.0.0.0:8001
# Now access at http://127.0.0.1:8001/
```

**Database error?**
```powershell
python manage.py migrate
```

**Static files not loading?**
```powershell
python manage.py collectstatic --noinput
```

---

## 📊 File Structure (Key Files)

```
✅ services/views.py       → 143 lines (7 views: home, login, signup, logout, providers, detail, register)
✅ services/urls.py        → 14 lines (8 URL patterns)
✅ services/models.py      → ServiceProvider with 15+ fields
✅ templates/              → 8 professional HTML templates
✅ static/style_new.css    → 987 lines of responsive CSS
✅ URL_PATHS.md           → Complete URL reference
✅ AUTHENTICATION_SUMMARY.md → Auth system docs
✅ IMPLEMENTATION_COMPLETE.md → Full project status
```

---

## 🎯 Features Ready to Use

✅ User registration (email + password)
✅ User login (email-based)
✅ User logout
✅ Account types (Customer/Provider)
✅ Provider discovery & search
✅ Provider filtering (service, location, rating)
✅ Provider profiles
✅ Responsive design (mobile, tablet, desktop)
✅ Professional UI with gradients
✅ Static files (SVG icons, avatars)
✅ Database persistence
✅ Error handling & messages
✅ Git version control

---

## 💡 Pro Tips

1. **Use Django's URL tags in templates**
   ```html
   <a href="{% url 'providers' %}">Find Services</a>
   ```
   (Prevents broken links when URLs change)

2. **Add new providers from Django admin**
   ```
   http://127.0.0.1:8000/admin/
   Providers → Add Provider
   ```

3. **Test with different screen sizes**
   - Press F12 in browser
   - Click device toolbar
   - Test responsive at 480px, 768px, 1024px

4. **Check git status anytime**
   ```powershell
   git status
   ```

---

## 📞 Next Steps

1. **Review documentation** in `URL_PATHS.md`
2. **Test all user flows** (signup → login → explore)
3. **Create sample providers** to show data
4. **Review code** in `services/views.py` and templates
5. **Plan future features** (password reset, email verification, etc.)

---

## 🎉 You're All Set!

The FixNear platform is **fully functional and ready to use**. Start the server and explore!

```powershell
myenv\Scripts\Activate.ps1
python manage.py runserver 0.0.0.0:8000
```

Then open: **http://127.0.0.1:8000/**

---

*Last Updated: February 24, 2026*
*Status: ✅ Ready to Use*
