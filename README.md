# employees_django
First off, you are getting that error because you are starting a project within the same directory as the cloned project, this directory already contains an app with the name employees hence the name conflict.

As regards steps to running the project by other users , this should work.

## clone the project

`git clone https://github.com/Dolampochki/employees_django.git`

## create and start a a virtual environment (optional)

`virtualenv env --no-site-packages`

`source env/bin/activate`

## Install the project dependencies:

`pip install -r requirements.txt`

then run

`python manage.py migrate`
`create admin account`

`python manage.py createsuperuser`

then

`python manage.py makemigrations employees`

to makemigrations for the app then again run

`python manage.py migrate`

to start the development server

`python manage.py runserver`

Full installation here

**https://newbedev.com/how-to-run-cloned-django-project**
