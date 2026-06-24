#!/usr/bin/env bash
set -o errexit

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing requirements..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running migrations..."
python manage.py migrate

echo "==> Build complete!"
