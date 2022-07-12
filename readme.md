# Magic the Gathering Django ORM demo

## Install instructions
* clone the repo
* Make sure to use your favorite virtualenv 
* `pip install -r requirements.txt


## Class DB setup
* `python manage.py migrate`
* `python manage.py loaddata data/full_fixture.json`
* `python manage.py shell_plus` (just shell also works if you are missing django_extensions)
