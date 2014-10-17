cd $(dirname $0)

heroku apps:create barachiel
sh heroku/setup.sh
sh heroku/deploy.sh