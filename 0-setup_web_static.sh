#!/usr/bin/env bash
# Script to set up web_static on a server

# Update package list and install Nginx if not already installed
sudo apt-get update
if ! dpkg -l | grep -q nginx; then
    sudo apt-get -y install nginx
fi
sudo ufw allow "Nginx HTTP"

# Create the necessary directories
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a fake HTML file with simple content
echo "<html>
<head>
</head>
<body>
    Holberton School
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link, ensuring it is updated every time
sudo ln -sfn /data/web_static/releases/test/ /data/web_static/current

# Set ownership of /data/ directory to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve /data/web_static/current/ to /hbnb_static
CONF_PATH="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static" "$CONF_PATH"; then
    sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/; }' "$CONF_PATH"
fi

# Restart Nginx to apply the changes
sudo service nginx restart
