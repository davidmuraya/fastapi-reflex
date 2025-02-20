#!/bin/bash

# Navigate to the project directory
cd /usr/share/nginx/fastapi-reflex/ || exit

# Update the repository
git fetch --all
git reset --hard origin/main

# Activate the virtual environment
source  . venv/bin/activate

# Install the requirements
pip install -r requirements.txt

# Navigate to the required folder
cd app/frontend/customer_app/ || exit

# Run Reflex export command (frontend-only)
reflex export --no-zip --frontend-only

# Restart the services
sudo systemctl restart fastapi-reflex reflex-backend

# deactivate the virtual environment
deactivate

echo "Deployment completed!"
