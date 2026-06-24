# 🚀 Render Deployment - Quick Start

## 📋 Pre-Deployment Checklist

✅ All files ready:
- `requirements.txt` - Python dependencies
- `build.sh` - Build script for Render
- `runtime.txt` - Python version (3.11.5)
- `.env.example` - Example environment variables
- Updated `settings.py` - Production-ready configuration

## 🔥 Quick Deploy Steps

### 1. Push to GitHub (5 minutes)
```bash
cd service_platform
git init
git add .
git commit -m "Ready for Render deployment"
```

Create repo on GitHub, then:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### 2. Create Database on Render (2 minutes)
1. Go to https://dashboard.render.com
2. Click **New +** → **PostgreSQL**
3. Name: `service-platform-db`
4. Instance: **Free**
5. Click **Create Database**
6. 📝 **Copy the Internal Database URL**

### 3. Create Web Service (3 minutes)
1. Click **New +** → **Web Service**
2. Connect your GitHub repo
3. Configure:
   - **Name**: `service-platform` (or your choice)
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn service_platform.wsgi:application`
   - **Instance Type**: **Free**

### 4. Add Environment Variables
Click **Advanced**, add these:

```
SECRET_KEY = [Generate new one at https://djecrety.ir/]
DEBUG = False
ALLOWED_HOSTS = service-platform.onrender.com
DATABASE_URL = [Paste Internal Database URL from Step 2]
CSRF_TRUSTED_ORIGINS = https://service-platform.onrender.com
PYTHON_VERSION = 3.11.5
```

5. Click **Create Web Service**

### 5. Wait & Watch (5-10 minutes)
- Render will build and deploy
- Watch the logs for any errors
- First deploy takes longer

### 6. Create Admin User
Once deployed:
1. Go to your service in Render dashboard
2. Click **Shell** tab
3. Run:
```bash
python manage.py createsuperuser
```
Enter:
- Email: `admin@servicehub.com`
- Password: `admin123`
- Role: `admin`

## ✅ Done!

Your site is live at: `https://service-platform.onrender.com`

Login at: `https://service-platform.onrender.com/login/`

---

## 🔄 To Update Your Site

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render auto-deploys in 3-5 minutes!

---

## ⚠️ Important Notes

**Free Tier Sleeps**: Site sleeps after 15 min of inactivity. First request takes 30-60 seconds to wake up.

**Media Files**: Uploaded files don't persist on free tier. Use Cloudinary for production.

**Database**: Free PostgreSQL has 90-day retention, no backups.

---

## 🆘 Common Issues

**Build Failed?**
- Check logs in Render dashboard
- Verify all files are committed and pushed

**Database Error?**
- Verify DATABASE_URL is correct
- Check database is running

**CSRF Error?**
- Add your URL to CSRF_TRUSTED_ORIGINS
- Use https:// prefix

**Static Files Missing?**
- Check build logs for collectstatic output
- WhiteNoise is configured automatically

---

For detailed instructions, see `DEPLOYMENT_GUIDE.md`
