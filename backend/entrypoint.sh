#!/bin/sh
set -e
echo $environment > .env.example
sed 's/ \([^ ]*=\)/\n\1/g' .env.example > .env
service ssh start
python manage.py makemigrations
python manage.py migrate 
exec python manage.py runserver 0.0.0.0:80