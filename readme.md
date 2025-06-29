# Magic the Gathering Django ORM demo

## Install instructions
* clone the repo
* Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you haven't already
* `uv sync` (creates virtual environment and installs dependencies)

### Alternative installation (traditional pip method)
* Make sure to use your favorite virtualenv 
* `pip install -r requirements.txt`

## Class DB setup
* `uv run python manage.py migrate`
* `uv run python manage.py loaddata data/full_fixture.json`
* `uv run python manage.py shell_plus` (just shell also works if you are missing django_extensions)


## PythonAnywhere Deployment
* Deploying code to the server: [https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/]
* Using environment variables: [https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/]
