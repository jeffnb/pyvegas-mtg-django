# Magic the Gathering Django ORM demo

## Install instructions with uv (Recommended)
* Clone the repo
* Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you haven't already
* `uv sync` - This will create a virtual environment and install all dependencies
* Activate the environment: `source .venv/bin/activate` (or use `uv run` prefix for commands)

## Legacy Install instructions (pip/virtualenv)
* Clone the repo
* Make sure to use your favorite virtualenv 
* `pip install -r requirements.txt`

## Class DB setup
* `uv run python manage.py migrate` (or `python manage.py migrate` if venv activated)
* `uv run python manage.py loaddata data/full_fixture.json` 
* `uv run python manage.py shell_plus` (django_extensions included in dev dependencies)

## Development Commands
* Run server: `uv run python manage.py runserver`
* Run migrations: `uv run python manage.py migrate`
* Create superuser: `uv run python manage.py createsuperuser`
* Django shell: `uv run python manage.py shell_plus`

## Adding Dependencies  
* Add runtime dependency: `uv add package-name`
* Add dev dependency: `uv add --dev package-name`
* Update dependencies: `uv lock --upgrade`

## PythonAnywhere Deployment
* Deploying code to the server: [https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/]
* Using environment variables: [https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/]
