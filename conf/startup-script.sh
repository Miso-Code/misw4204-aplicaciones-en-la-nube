#!/bin/bash

sudo apt update && sudo apt install -y libpq-dev nginx python3-pip

sudo systemctl start nginx
sudo systemctl enable nginx

sudo rm /etc/nginx/sites-available/*
sudo rm /etc/nginx/sites-enabled/*

ROOTDIR=/home/ubuntu/cloud_app
sudo cp $ROOTDIR/conf/nginx/flask.conf /etc/nginx/sites-available/default
sudo cp $ROOTDIR/conf/nginx/nginx.conf /etc/nginx/nginx.conf

sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

sudo systemctl restart nginx

cd $ROOTDIR/app
sudo pip install -r requirements.txt
sudo echo "Running server..."
sudo DB_URI=postgresql+psycopg2://myuser:mypassword@10.59.240.3:5432/appdb BROKER_URL=redis://10.128.0.4:6379/0 gunicorn app:app -w 4 --access-logfile - --error-logfile - --log-level info
