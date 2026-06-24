# 🚀 Deploy to Render - Simple Guide

## Step 1: Push to GitHub (5 min)

```bash
cd c:\Users\fombu\OneDrive\Desktop\service\service_platform
git add .
git commit -m "Ready for deployment"
git push origin main
```

If you don't have a GitHub repo yet:
1. Create repo at https://github.com/new
2. Run:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

## Step 2: Create Database on Render (2 min)

1. Go to https://dashboard.render.com
2. Click **New +** → **PostgreSQL**
3. Settings:
   - Name: `service-platform-db`
   - Instance: **Free**
4. Click **Create Database**
5. **COPY the "Internal Database URL"** - you'll need it!

---

## Step 3: Create Web Service (3 min)

1. Click **New +** → **Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `service-platform` (your URL will be: service-platform.onrender.com)
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT service_platform.wsgi:application`
   - **Instance Type**: **Free**

---

## Step 4: Add Environment Variables (2 min)

Click **Advanced**, then add these 5 variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate at https://djecrety.ir/ |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `service-platform.onrender.com` |
| `DATABASE_URL` | Paste the Internal URL from Step 2 |
| `CSRF_TRUSTED_ORIGINS` | `https://service-platform.onrender.com` |

Click **Create Web Service**

---

## Step 5: Wait for Build (10 min)

Watch the logs. You should see:
- ✅ Installing dependencies
- ✅ Collecting static files
- ✅ Running migrations
- ✅ Starting gunicorn

---

## Step 6: Create Admin User (2 min)

1. In Render dashboard, click **Shell** tab
2. Run:
```bash
python manage.py createsuperuser
```
3. Enter:
   - Email: `admin@servicehub.com`
   - Password: `admin123`
   - Role: `admin`

---

## ✅ Done!

Your site: `https://service-platform.onrender.com`

Login: `https://service-platform.onrender.com/login/`

---

## ⚠️ If Build Fails

### Common Fix: Pillow Error

If you get Pillow build errors, the requirements.txt has been simplified to fix this.

Make sure you pushed the latest code:
```bash
git add .
git commit -m "Fix build"
git push origin main
```

Render will auto-rebuild.

### Still Having Issues?

Check `docs/RENDER_TROUBLESHOOTING.md` for more solutions.

---

## 🔄 To Update Your Site Later

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render automatically redeploys in 3-5 minutes!
