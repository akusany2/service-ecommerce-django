#!/usr/bin/env bash

# Install libaries
cd /var/www/serviceapp
virtualenv -p python3 venv
source venv/bin/activate
python -m pip install gunicorn
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input

# Set permission for all files
sudo chown -R www-data:www-data /var/www/

# Restart services
# sudo -Hu www-data chmod a+x /var/www/serviceapp/server_configs/scripts/gunicorn_django.sh
gunicorn serviceecomm.wsgi
sudo service supervisor restart
sudo service nginx restart