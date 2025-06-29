# Agent Instructions

This document provides instructions for AI agents working with this codebase.

## Development Environment

This project uses `uv` for managing Python virtual environments and dependencies.

### Setting up the environment:

1.  **Install uv**:
    If you don't have `uv` installed, follow the instructions on the [official uv installation guide](https://github.com/astral-sh/uv#installation).

2.  **Create and activate virtual environment**:
    ```bash
    uv venv  # Creates .venv
    source .venv/bin/activate # Or relevant activation script for your shell
    ```

3.  **Install dependencies**:
    ```bash
    uv pip install -r requirements.txt
    ```

### Dependency Management with uv:

*   **To add a new dependency**:
    1.  Install the package: `uv pip install <package-name>`
    2.  Update `requirements.txt`: `uv pip freeze > requirements.txt`

*   **To remove a dependency**:
    1.  Remove the package from `requirements.txt`.
    2.  Sync the environment: `uv pip sync requirements.txt`

*   **To update dependencies**:
    1.  Update all packages: `uv pip install --upgrade -r requirements.txt`
    2.  Or update a specific package: `uv pip install --upgrade <package-name>`
    3.  Update `requirements.txt`: `uv pip freeze > requirements.txt`

Always ensure `requirements.txt` is up-to-date with the packages required by the project.

## Running Tests

[Instructions for running tests will go here once testing is set up.]

## Coding Conventions

[Details about coding style, linting, formatting, etc., will go here.]

## Deployment

[Information about deploying the application will go here.]
