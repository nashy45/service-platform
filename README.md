# Service Platform - Django Web Application

A professional service marketplace platform built with Django where customers can book services from approved providers.

## Features

- ✅ User Registration (Customer/Provider/Admin roles)
- ✅ Provider Approval System
- ✅ Service Management (CRUD for providers)
- ✅ Booking System with Status Tracking
- ✅ Review & Rating System
- ✅ Custom Dashboards for each role
- ✅ Password Reset (on-site)
- ✅ Provider Availability Toggle
- ✅ Real-time Statistics
- ✅ Currency: FCFA (Francs CFA)
- ✅ Fully Offline (Tailwind CSS + Font Awesome local)

## Tech Stack

- **Backend**: Django 5.1
- **Frontend**: Tailwind CSS, Font Awesome, JavaScript
- **Database**: SQLite (local), PostgreSQL (production)
- **Authentication**: Django Allauth
- **Forms**: Django Crispy Forms with Tailwind
- **Server**: Gunicorn (production)

## 🚀 Deploy to Render (FREE)

**Quick Deploy**: Open `docs/DEPLOYMENT_CHECKLIST.txt` and follow the steps.

### Requirements
- GitHub account
- Render account (free at https://render.com)
- 20 minutes

### Deployment Files
- `requirements.txt` - Python dependencies
- `build.sh` - Build script for Render
- `runtime.txt` - Python 3.11.9
- `.env.example` - Environment variables template

### Documentation
All guides are in the `docs/` folder:
- `DEPLOYMENT_CHECKLIST.txt` - Step-by-step checklist ⭐ **START HERE**
- `RENDER_QUICK_START.md` - Quick reference
- `DEPLOYMENT_GUIDE.md` - Complete detailed guide
- `RENDER_TROUBLESHOOTING.md` - Common issues & solutions

## 🏃 Local Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Migrations
```bash
python manage.py migrate
```

### Create Admin User
```bash
python manage.py createsuperuser
```

### Run Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## 📁 Project Structure

```
service_platform/
├── manage.py
├── requirements.txt
├── build.sh
├── runtime.txt
├── .env.example
├── db.sqlite3 (local only)
├── docs/                    # Documentation
├── service_platform/        # Django settings
├── accounts/                # User management
├── services/                # Service listings
├── bookings/                # Booking system
├── payments/                # Payment processing
├── reviews/                 # Review system
├── static/                  # CSS, JS, Font Awesome
├── templates/               # HTML templates
└── media/                   # User uploads
```

## 🔑 Default Admin Credentials (Local)

- Email: `admin@servicehub.com`
- Password: `admin123`

## 🌐 After Deployment

1. Create admin user via Render Shell
2. Add service categories via admin
3. Register test providers
4. Approve providers
5. Providers add services
6. Customers can book services

## 📝 License

This project is for educational/personal use.

## 🆘 Need Help?

- Local issues: Check Django documentation
- Deployment issues: See `docs/RENDER_TROUBLESHOOTING.md`
- Render support: https://community.render.com
