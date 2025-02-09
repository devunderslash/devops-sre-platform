#!/bin/sh
# sh file to configure the db from flask

if [ -d "migrations" ]; then
    # remove the migrations folder if exists
    rm -rf migrations
fi

echo "Running DB migrations"

set -e 

flask db init
flask db stamp head
flask db migrate -m "initial migration"
flask db upgrade

echo "DB migrations complete"

# gunicorn -b 0.0.0.0:8000 --timeout 600 wsgi:app
gunicorn -b 0.0.0.0:5001 wsgi:app