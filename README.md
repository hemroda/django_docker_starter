# Django Docker Starter

## Setting up the app

Clone the repo.

First run:

```sh
❯ docker-compose build
```

## Running the app

```sh
❯ docker-compose up
```

Open a browser to `http://127.0.0.1:8000/`

Enjoy the headaches 😁

## How to

### Create a Superuser

```sh
❯ docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

### Create new apps

Create an empty folder with the apps name first in `app/apps/name_of_the_app` then run:

```sh
❯ docker-compose run --rm app sh -c "python manage.py startapp name_of_the_app ./apps/name_of_the_app"
```

### Makemigrations

```sh
❯ docker-compose run --rm app sh -c "python manage.py makemigrations"
```

### Run Migrations

```sh
❯ docker-compose run --rm app sh -c "python manage.py migrate"
```

### Open the shell

```sh
❯ docker-compose run --rm app sh -c "python manage.py shell"
```

### Run tests

To run all the tests.

```sh
❯ docker-compose run --rm app sh -c "python manage.py test apps/*"
```

Or run the following for a specif app in the project.

```sh
❯ docker-compose run --rm app sh -c "python manage.py test apps/name_of_the_app"
```

## Locally test deployment (prod)

```sh
❯ docker-compose -f docker-compose-deploy.yml down --volumes
❯ docker-compose -f docker-compose-deploy.yml build
❯ docker-compose -f docker-compose-deploy.yml up
```

❗️Don't forget to kill the "prod" volumes after testing. (Run the first command)

### Create a Superuser when locally testing deployment (prod)

```sh
❯ docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py createsuperuser"
```

## Deploying in Prod

### Deploying in Prod for the first time

```sh
❯ cp .env.sample .env
```

Then update everything except the `DB_USER` value.

Now you can run the app:

```sh
❯ docker-compose -f docker-compose-deploy.yml up -d
```

### Deploying in Prod for updates

* SSH to the server.
* cd into `django_docker_starter` folder
* Pull the changes, run `git pull origin main`
* Run the following commands:

```sh
❯ docker-compose -f docker-compose-deploy.yml build app
❯ docker-compose -f docker-compose-deploy.yml up --no-deps -d app
```
