# Deploying to Render

This guide will help you deploy your Service Platform to Render for free.

## Prerequisites

1. A GitHub account (to host your code)
2. A Render account (sign up at https://render.com)
3. Git installed on your computer

## Step 1: Prepare Your Code

Your code is already configured for deployment. Make sure all files are saved.

## Step 2: Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., "service-platform")
3. **Do NOT** initialize with README (your project already has files)
4. Copy the repository URL

## Step 3: Push Code to GitHub

Open your terminal in the `service_platform` folder and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - Service Platform ready for deployment"

# Add your GitHub repository as remote (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/service-platform.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Deploy on Render

### Option A: Using render.yaml (Automatic)

1. Log in to your Render dashboard: https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account (if not already connected)
4. Select your **service-platform** repository
5. Render will detect `render.yaml` and configure everything automatically
6. Click **"Apply"**
7. Wait for the build to complete (5-10 minutes)

### Option B: Manual Setup

1. Log in to Render: https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** service-platform (or any name you like)
   - **Runtime:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn service_platform.wsgi:application`
   - **Plan:** Free

5. Add Environment Variables (click "Advanced" → "Add Environment Variable"):
   ```
   DEBUG=False
   SECRET_KEY=<click "Generate" to create a secure key>
   ALLOWED_HOSTS=.onrender.com
   CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
   ```

6. Click **"Create Web Service"**

7. Create a PostgreSQL Database:
   - Go to Dashboard → **"New +"** → **"PostgreSQL"**
   - Name: service-platform-db
   - Plan: Free
   - Click **"Create Database"**
   - Once created, copy the **"Internal Database URL"**
   - Go back to your Web Service → Environment → Add:
     ```
     DATABASE_URL=<paste the internal database URL here>
     ```

## Step 5: Update CSRF_TRUSTED_ORIGINS

Once your app is deployed, Render will give you a URL like:
`https://service-platform-abcd.onrender.com`

Update the environment variable:
1. Go to your Web Service settings
2. Find **CSRF_TRUSTED_ORIGINS**
3. Update to: `https://service-platform-abcd.onrender.com` (use your actual URL)
4. Save (this will trigger a redeploy)

## Step 6: Create Admin User

After deployment completes:

1. Go to your Render dashboard
2. Click on your web service
3. Click **"Shell"** (top right)
4. Run these commands:

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

## Step 7: Test Your Site

Visit your Render URL (e.g., `https://service-platform-abcd.onrender.com`)

Your site should be live! 🎉

## Important Notes

### Free Tier Limitations

- **Cold starts:** Free apps sleep after 15 minutes of inactivity. First request may take 30-60 seconds.
- **Database:** 90 days free, then $7/month for PostgreSQL, or stays free if you migrate data within 90 days
- **Build minutes:** 500 minutes/month free

### Your SQLite Data

The SQLite database (`db.sqlite3`) with your local test data will **NOT** be deployed. Render uses PostgreSQL in production. You'll need to:

1. Create a new admin user (as shown in Step 6)
2. Recreate any test data through the admin dashboard or forms

### Updating Your Site

Whenever you make changes to your code:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Render will automatically detect the push and redeploy your app.

## Troubleshooting

### Build Failed

- Check the build logs in Render dashboard
- Common issues:
  - Missing dependencies in `requirements.txt`
  - Syntax errors in Python code
  - Build command permissions (make sure `build.sh` is executable)

### Site Shows 500 Error

- Check application logs in Render dashboard
- Verify all environment variables are set correctly
- Make sure `DEBUG=False` in production
- Check `ALLOWED_HOSTS` includes your Render domain

### Static Files Not Loading

- Verify `npm run build-css` ran successfully during build
- Check that `collectstatic` ran without errors
- WhiteNoise should serve static files automatically

### Database Connection Error

- Verify `DATABASE_URL` environment variable is set correctly
- Make sure your PostgreSQL database is running
- Check database connection string format

## Need Help?

- Render Documentation: https://render.com/docs
- Django Deployment Checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

## Cost Breakdown (Free Tier)

- Web Service: **Free** (with cold starts)
- PostgreSQL: **Free for 90 days**, then $7/month
- Total: **$0/month** for first 90 days

After 90 days, you can:
1. Pay $7/month for PostgreSQL
2. Export data and recreate free database
3. Switch to another free tier service
