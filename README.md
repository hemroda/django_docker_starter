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


## Locally test deployment (prod)

```
$ docker-compose -f docker-compose-deploy.yml down --volumes
$ docker-compose -f docker-compose-deploy.yml build
$ docker-compose -f docker-compose-deploy.yml up
```
❗️Don't forget to kill the "prod" volumes after testing. (Run the first command)


#### Create a Superuser when locally testing deployment (prod)

`$ docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py createsuperuser"`