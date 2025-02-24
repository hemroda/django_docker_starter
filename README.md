# django_docker_starter

A repo to kickstart your Django Project

## Technologies

| Backend | Frontend   | DevOps    | Data       | Project Management | Tools |
|---------|------------|-----------|------------|--------------------|-------|
| Python  | HTMX       | Docker    | PostgreSQL | GitHub             | uv    |
| Django  | JavaScript | CI/CD     | SQLAlchemy |                    | npm   |
| Pytest  | CSS        | Terraform | pgAdmin    |                    |       |
|         | HTML5      | Hetzner   |            |                    |       |
|         |            |           |            |                    |       |

## TODO

Change:
* Search and replace `your-url.com;` with your URL.
* Search and replace `django_docker_starter` with your project's name.
* Change `main.tf` if you are not deploying on Hetzner.

## DEV

```sh
git clone git@github.com:hemroda/django_docker_starter.git
```

* Install [uv](https://github.com/astral-sh/uv)

```sh
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

* Environment variables

```sh
cp .env.sample .env
cp ./django-app/.env.sample ./django-app/.env
cp ./fastapi-api/.env.sample ./fastapi-api/.env
```

* Build the project using Docker

```sh
docker-compose up -d --build
```

==> For Django, go to [http://localhost:8080](http://localhost:8080)
==> For FastAPI, go to [http://localhost:8000](http://localhost:8000)

* Pre-commit

```sh
pip install pre-commit
```

### DJANGO

⚠️ Make sure you are in the `django-app` directory.

#### Install new package

```sh
uv add name-of-package
uv add name-of-package --dev
```

#### Migrations

* List the migrations

```sh
docker-compose exec django-app python manage.py showmigrations
```

* If your changes are not listed, create a migration file for it

```sh
docker-compose exec django-app python manage.py makemigrations
```

* Run the migrations

```sh
docker-compose exec django-app python manage.py migrate --noinput
```

⚠️ If you try to make your migration files and nothing happens chances are that you created a new model in a `models`
folder. which means you need to add the newly created model to the imports in `the_app/models/__init__.py` file.

Example in `django-app/apps/app-name`, you just created the `Task` model, you would add it this way:

```py
from .project import Project
from .task import Task

__all__ = ["Project", "Task"]
```

Now re-run the 2 commands above.

* Ensure the default Django tables were created:

See [Database](#database) section bellow.

#### Access the shell

```sh
docker-compose exec django-app python manage.py shell_plus
```

#### Create new Django app

⚠️ Make sure you create the folder for the new app, then:

```sh
mkdir apps/name_of_the_app
docker-compose exec django-app python manage.py startapp name_of_the_app ./apps/name_of_the_app
```

#### Create a Superuser

```sh
docker-compose run --rm django-app sh -c "python manage.py createsuperuser"
```

#### Test accounts:

There few accounts created during the seed process:

* For admin section:

  url: [http://localhost:8080/admin](http://localhost:8080/admin)

  username: `admin`

  password: `password`

* For non superuser (accounts):

  url: [http://localhost:8080/login](http://localhost:8080/login)

  username: `seconduser`

  password: `password`

These logins are usable in development.

### Database

#### Access the database from the CLI:

```sh
docker-compose exec db psql --username=pguser --dbname=django_docker_starter_db
```

#### Access pgAdmin

Go to `http://localhost:4000/login`

Use the following logins:

    - user/email: admin@users.com

    - password: adminpassword

When creating the server:

- General tab:

        - name: server

  - Connection tab:

    - Host name/address: db

    - Username: pguser

    - Password: pguserpassword

    ⚠️ The other fields do not change

## PRODUCTION

### Deploying in Prod for updates

* SSH to the server.
* cd into `django_docker_starter` folder
* Pull the changes, run `git pull origin main`
* Run the following commands:

```sh
docker-compose -f docker-compose-prod.yml up -d --build
```

If only `django-app` was updated, run:

```sh
docker-compose -f docker-compose-prod.yml up -d --build django-app
```

### Create a Superuser

```sh
docker-compose exec django-app python manage.py createsuperuser
```
