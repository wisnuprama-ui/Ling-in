migrate: bash deployment.sh
web: gunicorn ling_in.wsgi --log-file -
heroku ps:scale web=1 migrate=1 --app