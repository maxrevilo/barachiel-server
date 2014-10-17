DB_NAME=$(heroku config | grep POSTGRESQL | awk '{print $1;}' | sed "s/.....$//")
echo "Erasing database "$DB_NAME
heroku pg:reset $DB_NAME