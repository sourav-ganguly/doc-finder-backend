#!/bin/bash

# Script to run Ruff linter and formatter locally

# Check if Ruff is installed
if ! command -v ruff &> /dev/null; then
    echo "Ruff is not installed. Installing now..."
    pip install ruff
fi

echo "Running Ruff linter..."
ruff check .

echo -e "\nRunning Ruff formatter check..."
ruff format --check .

# Ask if user wants to apply formatting fixes
read -p "Do you want to apply formatting fixes? (y/n): " apply_fixes

if [[ $apply_fixes == "y" || $apply_fixes == "Y" ]]; then
    echo "Applying formatting fixes..."
    ruff format .
    echo "Formatting fixes applied."
fi

echo -e "\nLinting and formatting check completed." 