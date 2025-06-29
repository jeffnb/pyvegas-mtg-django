# Magic the Gathering Django ORM demo

## Install instructions
* clone the repo
* Make sure to use your favorite virtualenv 
* `pip install -r requirements.txt`

## Using uv (Recommended)

`uv` is a fast Python package installer and resolver, written in Rust. It's a drop-in replacement for pip and pip-tools.

### Setup with uv

1.  **Install uv**:
    Follow the instructions on the [official uv installation guide](https://github.com/astral-sh/uv#installation) to install `uv` on your system.

2.  **Create a virtual environment**:
    ```bash
    uv venv
    ```
    This will create a virtual environment named `.venv` in your project directory.

3.  **Activate the virtual environment**:
    ```bash
    source .venv/bin/activate
    ```

4.  **Install dependencies**:
    ```bash
    uv pip install -r requirements.txt
    ```

### Managing Dependencies with uv

*   **Adding a new dependency**:
    ```bash
    uv pip install <package-name>
    ```
    Then, update your `requirements.txt`:
    ```bash
    uv pip freeze > requirements.txt
    ```

*   **Removing a dependency**:
    First, remove the package from your `requirements.txt` file.
    Then, sync your environment:
    ```bash
    uv pip sync requirements.txt
    ```

*   **Updating dependencies**:
    ```bash
    uv pip install --upgrade -r requirements.txt
    ```
    Or, to upgrade a specific package:
    ```bash
    uv pip install --upgrade <package-name>
    ```
    Remember to update `requirements.txt` after upgrading:
    ```bash
    uv pip freeze > requirements.txt
    ```


## Class DB setup
* `python manage.py migrate`
* `python manage.py loaddata data/full_fixture.json`
* `python manage.py shell_plus` (just shell also works if you are missing django_extensions)


## PythonAnywhere Deployment
* Deploying code to the server: [https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/]
* Using environment variables: [https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/]
