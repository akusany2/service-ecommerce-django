#!/usr/bin/env bash

sudo yum update
sudo yum install -y python3 python-dev python3-pip ffmpeg supervisor nginx
pip install --user --upgrade virtualenv
sudo rm -rf /var/www/serviceapp