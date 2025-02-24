#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python3 manage.py migrate

if [ "$ENVIRONMENT" = "development" ]
then
    echo "Seeding STARTED..."
    python manage.py loaddata apps/accounts/fixtures/seed_accounts.json
    echo "Seeding FINISHED."

    # Run Django development server
    exec python manage.py runserver_plus 0.0.0.0:8000
else
    # Clear existing static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear

    exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
fi
