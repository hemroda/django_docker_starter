Django Docker Starter
===

## Setting up the app

Clone the repo.  

First run `$ docker-compose build`  

`$ mkdir data` creating folder for static files in dev mode.


## Running the app

Run `$ docker-compose up` then open a browser to `http://127.0.0.1:8000/`  


Enjoy the headaches 😁


## How to

#### Create a Superuser

`$ docker-compose run --rm app sh -c "python manage.py createsuperuser"`


#### Create apps

Create an empty folder with the apps name first in `backend/apps/name_of_the_app` then run:  
`$ docker-compose run --rm app sh -c "python manage.py startapp name_of_the_app ./apps/name_of_the_app"`


#### Makemigrations

`$ docker-compose run --rm app sh -c "python manage.py makemigrations"`


#### Run Migrations

`$ docker-compose run --rm app sh -c "python manage.py migrate"`


#### Open the shell

`$ docker-compose run --rm app sh -c "python manage.py shell"`


#### Run tests

Run `$ docker-compose run --rm app sh -c "python manage.py test apps/*"` for all the tests.  
Or run `$ docker-compose run --rm app sh -c "python manage.py test apps/name_of_the_app"` for specif app.


## Locally test deployment (prod)

```
$ docker-compose -f docker-compose-deploy.yml down --volumes
$ docker-compose -f docker-compose-deploy.yml build
$ docker-compose -f docker-compose-deploy.yml up
```
❗️Don't forget to kill the "prod" volumes after testing. (Run the first command)


#### Create a Superuser when locally testing deployment (prod)

`$ docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py createsuperuser"`

## Deploying in Rpod

* SSH to the server.
* Pull the changes, run `$ git pull origin`
* Run the following commands:

```sh
$ docker-compose -f docker-compose-deploy.yml build app
$ docker-compose -f docker-compose-deploy.yml up --no-deps -d app
```
