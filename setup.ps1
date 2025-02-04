# Install uv if not already installed
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
}

# Create and activate virtual environment
Write-Host "Creating virtual environment with uv..."
uv venv

# Install dependencies
Write-Host "Installing dependencies..."
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt

# Initialize pre-commit
Write-Host "Setting up pre-commit hooks..."
pre-commit install

Write-Host "Setup complete! You can now commit changes and pre-commit hooks will run automatically."