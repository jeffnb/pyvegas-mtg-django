# Magic the Gathering Django ORM demo

## Install instructions
* Clone the repo
* Make sure to use your favorite virtualenv 
* Install dependencies using uv:
  * `uv pip install -e .`  # Installs the project in development mode
  * Alternatively: `uv pip sync`  # Syncs dependencies from pyproject.toml

## Using uv
This project uses [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver written in Rust.

### Why uv?
We've transitioned from pip to uv for several benefits:
- **Speed**: uv is significantly faster than pip for installing packages
- **Reliability**: uv provides more reliable dependency resolution
- **Compatibility**: uv works with existing Python projects and tools
- **Modern**: uv supports modern Python packaging standards with pyproject.toml

The project still maintains compatibility with pip through the requirements.txt file, but uv is recommended for the best experience.

### Quick Start with uv
For convenience, a setup script is provided that will:
1. Install uv if not already installed
2. Create and activate a virtual environment
3. Install all dependencies
4. Set up the database

```bash
# Make the script executable
chmod +x uv.sh

# Run the setup script
./uv.sh
```

### Manual Installation with uv
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv

# Create a virtual environment
uv venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -e .
```


## Class DB setup
* `python manage.py migrate`
* `python manage.py loaddata data/full_fixture.json`
* `python manage.py shell_plus` (just shell also works if you are missing django_extensions)


## PythonAnywhere Deployment
* Deploying code to the server: [https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/]
* Using environment variables: [https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/]
