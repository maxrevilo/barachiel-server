cd $(dirname $0)

heroku apps:create barachiel
sh setup.sh
sh deploy.sh