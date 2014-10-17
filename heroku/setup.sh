#!/bin/bash
exec > /dev/null 2>&1

SECRET_KEY=$(openssl rand -base64 64)

heroku config:set DJANGO_ENV=heroku
heroku config:set DJANGO_SECRET_KEY=$SECRET_KEY
heroku config:set DJANGO_DEBUG=False