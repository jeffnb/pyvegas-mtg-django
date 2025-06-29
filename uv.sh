#!/bin/bash
# Helper script for setting up and using uv with the Magic the Gathering Django ORM demo

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Magic the Gathering Django ORM demo - uv setup helper${NC}"
echo

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}uv not found. Installing...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Make sure uv is in the PATH
    export PATH="$HOME/.cargo/bin:$PATH"
    echo "uv installed successfully!"
else
    echo "uv is already installed."
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    uv venv .venv
    echo "Virtual environment created at .venv/"
else
    echo "Using existing virtual environment at .venv/"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
uv pip install -e .
echo "Dependencies installed successfully!"

# Setup database if needed
if [ ! -f "db.sqlite3" ]; then
    echo -e "${YELLOW}Setting up database...${NC}"
    python manage.py migrate
    python manage.py loaddata data/full_fixture.json
    echo "Database setup complete!"
fi

echo
echo -e "${GREEN}Setup complete!${NC}"
echo "You can now run the project with: python manage.py runserver"
echo "To activate the virtual environment in the future, run: source .venv/bin/activate"