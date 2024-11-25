#!/bin/bash

# Exit on any error
set -e

echo "Starting deployment..."

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
pip install -r requirements.txt

# Run database migrations
flask db upgrade

# Restart the application
sudo systemctl restart bloggers

echo "Deployment completed successfully!"
