#!/bin/bash

# Exit on any error
set -e

echo "Starting server setup..."

# Install required packages
apt-get update
apt-get install -y python3-pip python3-venv nginx mysql-server

# Create nginx configuration
cat > /etc/nginx/sites-available/bloggers << 'EOL'
server {
    listen 80;
    server_name 161.35.22.52;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOL

# Enable the site
ln -sf /etc/nginx/sites-available/bloggers /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Move files to correct location
mkdir -p /var/www/bloggers
cp -r /root/bloggers/* /var/www/bloggers/
cd /var/www/bloggers

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Copy systemd service file
cp bloggers.service /etc/systemd/system/

# Reload systemd and start services
systemctl daemon-reload
systemctl restart nginx
systemctl enable bloggers
systemctl start bloggers

echo "Server setup completed!"
