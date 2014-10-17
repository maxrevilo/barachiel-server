#TODO: run grunt build on frontend/dev
git push heroku master
heroku ps:scale web=1
heroku run python manage.py syncdb
heroku run python manage.py migrate