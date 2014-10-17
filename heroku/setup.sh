#!/bin/bash
exec > /dev/null 2>&1

SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9_.,\-@#$()' | fold -w 50 | head -n 1)

heroku config:set DJANGO_ENV=heroku
heroku config:set DJANGO_SECRET_KEY=$SECRET_KEY
heroku config:set DJANGO_DEBUG=False