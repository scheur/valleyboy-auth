$ErrorActionPreference = "Stop"

# Set working directory to script location
Set-Location $PSScriptRoot

# Deploy using SAM
sam deploy `
    --stack-name valleyboy-auth `
    --region us-east-1 `
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND `
    --parameter-overrides DomainName=valleyboy.io