# Render Deployment Guide

## Prerequisites
- A Render account (free tier available at https://render.com)
- A GitHub or GitLab account
- Your project code pushed to a Git repository

## Step 1: Prepare Your Git Repository

1. **Initialize Git** (if not already done):
   ```bash
   cd service_platform
   git init
   git add .
   git commit -m "Initial commit - service platform ready for deployment"
   ```

2. **Create a GitHub repository**:
   - Go to https://github.com/new
   - Create a new repository (e.g., "service-platform")
   - Don't initialize with README, .gitignore, or license

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/service-platform.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Create PostgreSQL Database on Render

1. Log in to https://dashboard.render.com
2. Click **"New +"** button → Select **"PostgreSQL"**
3. Configure:
   - **Name**: `service-platform-db`
   - **Database**: `service_platform_db`
   - **User**: (auto-generated)
   - **Region**: Select closest to your users
   - **Instance Type**: `Free` (0GB RAM, shared CPU)
4. Click **"Create Database"**
5. Wait for database to be ready (takes ~1-2 minutes)
6. **Copy the Internal Database URL** - you'll need this later

## Step 3: Create Web Service on Render

1. Click **"New +"** → Select **"Web Service"**
2. Connect your GitHub repository:
   - Click **"Connect account"** if first time
   - Find and select your `service-platform` repository
   - Click **"Connect"**

3. Configure the web service:
   - **Name**: `service-platform` (this becomes your URL: service-platform.onrender.com)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `service_platform` (if your Django project is in a subfolder)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn service_platform.wsgi:application`
   - **Instance Type**: `Free` (512MB RAM, shared CPU)

4. Click **"Advanced"** to add environment variables:

   Add these environment variables one by one:

   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | Generate a new one: https://djecrety.ir/ |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `service-platform.onrender.com` (use your actual app name) |
   | `DATABASE_URL` | Paste the Internal Database URL from Step 2 |
   | `CSRF_TRUSTED_ORIGINS` | `https://service-platform.onrender.com` (use your actual app name) |
   | `PYTHON_VERSION` | `3.11.5` |

   **Optional** (if using Stripe payments):
   | Key | Value |
   |-----|-------|
   | `STRIPE_PUBLIC_KEY` | Your Stripe publishable key |
   | `STRIPE_SECRET_KEY` | Your Stripe secret key |

5. Click **"Create Web Service"**

## Step 4: Wait for Deployment

Render will now:
1. Clone your repository
2. Install dependencies from `requirements.txt`
3. Run `python manage.py collectstatic --no-input`
4. Run `python manage.py migrate`
5. Start the gunicorn server

This takes about 5-10 minutes for first deployment.

Watch the logs in the Render dashboard to see progress.

## Step 5: Create Admin User

Once deployment is complete:

1. In Render dashboard, click your web service
2. Go to **"Shell"** tab in the left sidebar
3. Click **"Launch Shell"**
4. Run these commands:
   ```bash
   python manage.py createsuperuser
   ```
5. Enter email: `admin@servicehub.com`
6. Enter password: `admin123` (or your preferred password)
7. When asked for role, type: `admin`

## Step 6: Access Your Live Site

Your site is now live at: `https://service-platform.onrender.com`

- Homepage: `https://service-platform.onrender.com/`
- Admin Login: `https://service-platform.onrender.com/login/`
- Login as: `admin@servicehub.com` / `admin123`

## Important Notes

### Free Tier Limitations
- **Sleep Mode**: Free services sleep after 15 minutes of inactivity
- **Wake Up**: First request after sleep takes ~30-60 seconds
- **Database**: 90 days retention on free tier
- **Storage**: Media files uploaded won't persist (use Cloudinary for production)

### Handling Media Files
On Render's free tier, uploaded media files don't persist between deploys or restarts.

**Solutions**:
1. **Use Cloudinary** (recommended for free tier):
   - Sign up at https://cloudinary.com (free tier available)
   - Get your Cloud Name, API Key, API Secret
   - Add them as environment variables in Render
   - Update settings.py to use Cloudinary storage

2. **Use Render Disks** (requires paid plan):
   - Add a persistent disk to your Render service
   - Mount at `/opt/render/project/src/media`

### Database Backups
- Free PostgreSQL databases are **NOT backed up**
- For important data, upgrade to a paid plan with automatic backups
- Or manually backup using:
  ```bash
  pg_dump $DATABASE_URL > backup.sql
  ```

### Updating Your Site

To deploy updates:
1. Make changes to your code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```
3. Render automatically detects the push and redeploys (takes 3-5 minutes)

### Custom Domain

To use your own domain:
1. In Render dashboard, go to your web service
2. Click **"Settings"** → **"Custom Domain"**
3. Add your domain (e.g., `www.yourdomain.com`)
4. Update your DNS records as shown by Render
5. Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` environment variables

## Troubleshooting

### Build Failed
- Check the build logs in Render dashboard
- Ensure `requirements.txt` has all dependencies
- Verify `build.sh` has correct commands

### Database Connection Error
- Verify `DATABASE_URL` environment variable is set correctly
- Ensure database and web service are in same region
- Check database is running in Render dashboard

### Static Files Not Loading
- Verify `collectstatic` ran successfully in build logs
- Check `STATIC_ROOT` is set to `staticfiles`
- WhiteNoise should be in MIDDLEWARE (already configured)

### CSRF Errors
- Add your Render URL to `CSRF_TRUSTED_ORIGINS` environment variable
- Format: `https://your-app-name.onrender.com` (include https://)

### Site is Slow
- First request after sleep takes 30-60 seconds (free tier)
- Consider upgrading to paid tier for always-on service
- Or use a service like UptimeRobot to ping your site every 5 minutes

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/

## Next Steps

1. Set up email service (SendGrid, Mailgun, etc.) for real email notifications
2. Configure Cloudinary for media file storage
3. Set up Stripe payments if needed
4. Add monitoring (Sentry for error tracking)
5. Consider upgrading to paid tier for production use
