#!/bin/bash
set -euo pipefail

# Duration for temporary credentials (in seconds)
DURATION=3600

# Retrieve temporary credentials using the active profile.
# (For AWS SSO credentials, this may differ; this example is for IAM user credentials.)
TEMP_CREDS=$(aws sts get-session-token --duration-seconds $DURATION --output json)

# Parse credentials (requires jq to be installed)
ACCESS_KEY=$(echo "$TEMP_CREDS" | jq -r '.Credentials.AccessKeyId')
SECRET_KEY=$(echo "$TEMP_CREDS" | jq -r '.Credentials.SecretAccessKey')
SESSION_TOKEN=$(echo "$TEMP_CREDS" | jq -r '.Credentials.SessionToken')

# Construct a JSON object required by the federation endpoint.
SESSION_JSON=$(printf '{"sessionId":"%s","sessionKey":"%s","sessionToken":"%s"}' "$ACCESS_KEY" "$SECRET_KEY" "$SESSION_TOKEN")

# URL-encode the JSON (using Python 3 for URL encoding)
SESSION_JSON_URLENCODED=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "$SESSION_JSON")

# Retrieve a sign-in token by calling the AWS federation endpoint
FEDERATION_URL="https://signin.aws.amazon.com/federation?Action=getSigninToken&Session=${SESSION_JSON_URLENCODED}"
SIGNIN_TOKEN_RESPONSE=$(curl -s "$FEDERATION_URL")
SIGNIN_TOKEN=$(echo "$SIGNIN_TOKEN_RESPONSE" | jq -r '.SigninToken')

# Specify the destination (the AWS Console) and URL-encode it.
DESTINATION=$(python3 -c "import urllib.parse; print(urllib.parse.quote('https://console.aws.amazon.com/'))")

# Construct the final login URL
LOGIN_URL="https://signin.aws.amazon.com/federation?Action=login&Issuer=&Destination=${DESTINATION}&SigninToken=${SIGNIN_TOKEN}"

echo "AWS Console URL:"
echo "$LOGIN_URL"

# Open the URL in the default web browser
if command -v xdg-open &>/dev/null; then
    xdg-open "$LOGIN_URL"
elif command -v open &>/dev/null; then
    open "$LOGIN_URL"
else
    echo "Please open the above URL in your browser."
fi
