#!/bin/bash

# Default filenames
DEFAULT_ENV_FILES=(".env" "input.env")

# Check for CLI arg --env-file
for arg in "$@"; do
  case $arg in
    --env-file=*)
      ENV_FILE="${arg#*=}"
      shift
      ;;
  esac
done

# Auto-detect if not specified
if [ -z "$ENV_FILE" ]; then
  for f in "${DEFAULT_ENV_FILES[@]}"; do
    if [ -f "./$f" ]; then
      ENV_FILE="./$f"
      break
    fi
  done
fi

# Load env file
if [ -n "$ENV_FILE" ] && [ -f "$ENV_FILE" ]; then
  echo "🔐 Loading environment variables from $ENV_FILE"
  set -a
  source "$ENV_FILE"
  set +a
else
  echo "⚠️  No env file found. Proceeding with manual input..."
fi


### OBTAIN KEYCLOAK ACCESS TOKEN ###############

# Validate required inputs
if [[ -z "$KEYCLOAK_URL" || -z "$REALM" || -z "$CLIENT_ID" || -z "$CLIENT_SECRET" ]]; then
  echo "❌ Error: One or more required variables are missing. Aborting."
  exit 1
fi

# Create the Basic Auth header (base64 encode "client_id:client_secret")
ENCODED_AUTH=$(echo -n "$CLIENT_ID:$CLIENT_SECRET" | base64)
AUTH_HEADER="Basic $ENCODED_AUTH"
GRANT_TYPE="client_credentials"

# Construct token endpoint URL
TOKEN_URL="${KEYCLOAK_URL%/}/realms/${REALM}/protocol/openid-connect/token"

echo "🔐 Requesting access token using client credentials..."

# Perform the curl request
RESPONSE=$(curl --silent --location "$TOKEN_URL" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --header "Authorization: Basic $AUTH_HEADER" \
  --data-urlencode "client_id=$CLIENT_ID" \
  --data-urlencode "client_secret=$CLIENT_SECRET" \
  --data-urlencode "grant_type=$GRANT_TYPE")

# Print response
if command -v jq >/dev/null 2>&1; then
  echo "$RESPONSE" | jq .
  # Extract access_token manually (fragile but functional)
  ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
else
  echo "$RESPONSE"
  # Extract access_token manually (fragile but functional)
  ACCESS_TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*"' | sed 's/"access_token":"\(.*\)"/\1/')
fi
echo "Access Token: $ACCESS_TOKEN"



### CREATE CONSUMER ##########

# Validate required inputs
if [[ -z "$OBP_CONSUMER_APP_NAME" || -z "$OBP_CONSUMER_APP_TYPE" || -z "$OBP_CONSUMER_DESC" || -z "$OBP_DEVELOPER_EMAIL"  || -z "$OBP_COMPANY"  || -z "$OBP_REDIRECT_URL"  || -z "$OBP_CREATED_BY_USER_ID"  || -z "$OBP_LOGO_URL"  || -z "$OBP_CLIENT_CERT" ]]; then
  echo "❌ Error: One or more required variables are missing. Aborting."
  exit 1
fi


# Construct API URL
OBP_API_URL="${OBP_BASE_URL%/}/obp/v5.1.0/management/consumers"

# Create JSON payload
read -r -d '' PAYLOAD << EOM
{
  "app_name": "$OBP_CONSUMER_APP_NAME",
  "app_type": "$OBP_CONSUMER_APP_TYPE",
  "description": "$OBP_CONSUMER_DESC",
  "developer_email": "$OBP_DEVELOPER_EMAIL",
  "company": "$OBP_COMPANY",
  "redirect_url": "$OBP_REDIRECT_URL",
  "created_by_user_id": "$OBP_CREATED_BY_USER_ID",
  "enabled": true,
  "created": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "client_certificate": "$OBP_CLIENT_CERT",
  "logo_url": "$OBP_LOGO_URL"
}
EOM

# Send the request
echo "📡 Sending request to $OBP_API_URL..."
JSON_RESPONSE=$(curl --silent --location "$OBP_API_URL" \
  --header "Authorization: Bearer $ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data-raw "$PAYLOAD")

# Output response (prettified if jq is installed)
if command -v jq >/dev/null 2>&1; then
  echo "$JSON_RESPONSE" | jq .
else
  echo "$JSON_RESPONSE"
fi

# Extract values using grep + sed (basic POSIX-safe)
CONSUMER_KEY=$(echo "$JSON_RESPONSE" | sed -n 's/.*"consumer_key":"\([^"]*\)".*/\1/p')
CONSUMER_SECRET=$(echo "$JSON_RESPONSE" | sed -n 's/.*"consumer_secret":"\([^"]*\)".*/\1/p')

# Output file
OUTPUT_FILE="output.env"

# Write to output.env
{
  echo "OBP_CONSUMER_KEY=$CONSUMER_KEY"
  echo "OBP_CONSUMER_SECRET=$CONSUMER_SECRET"
} > "$OUTPUT_FILE"

echo "✅ Exported to $OUTPUT_FILE:"
cat "$OUTPUT_FILE"
