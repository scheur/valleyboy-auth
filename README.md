# Valleyboy Auth

Authentication and chat service for valleyboy.io using Cognito and Claude 3.5 Sonnet.

## Development Setup

1. Install prerequisites:
   - Python 3.12 or higher
   - Git

2. Clone the repository:
   ```powershell
   git clone https://github.com/scheur/valleyboy-auth.git
   cd valleyboy-auth
   ```

3. Run the setup script:
   ```powershell
   .\setup.ps1
   ```

This will:
- Install uv package manager
- Create a virtual environment
- Install dependencies
- Set up pre-commit hooks

## Pre-commit Hooks

The following checks run automatically on commit:
- CloudFormation template validation (cfn-lint)
- YAML format checking
- Python code formatting (black)
- Basic file checks

## Build Process

The project uses AWS CodeBuild with the following stages:
1. Install dependencies with uv
2. Validate CloudFormation template
3. Package and deploy infrastructure

## Infrastructure

- Cognito User Pool with hosted UI
- API Gateway with Lambda backend
- Claude 3.5 Sonnet integration
- CloudFront distribution

## DNS Configuration

- auth-dev.valleyboy.io: Development environment
- auth.valleyboy.io: Production environment