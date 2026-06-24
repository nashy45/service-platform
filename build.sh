#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Build Tailwind CSS
npm install
npm run build-css

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
