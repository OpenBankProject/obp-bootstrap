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

# Prompt only if value is undefined or empty
[ -z "$OBP_BASE_URL" ] && read -p "Enter base API URL (e.g. http://127.0.0.1:8080/): " OBP_BASE_URL
[ -z "$OBP_EMAIL" ] && read -p "Enter email: " OBP_EMAIL
[ -z "$OBP_USERNAME" ] && read -p "Enter username: " OBP_USERNAME
[ -z "$OBP_PASSWORD" ] && read -s -p "Enter password (hidden): " OBP_PASSWORD && echo
[ -z "$OBP_FIRST_NAME" ] && read -p "Enter first name: " OBP_FIRST_NAME
[ -z "$OBP_LAST_NAME" ] && read -p "Enter last name: " OBP_LAST_NAME

# Validate required inputs
if [[ -z "$OBP_BASE_URL" || -z "$OBP_EMAIL" || -z "$OBP_USERNAME" || -z "$OBP_PASSWORD" || -z "$OBP_FIRST_NAME" || -z "$OBP_LAST_NAME" ]]; then
  echo "❌ Error: One or more required variables are missing. Aborting."
  exit 1
fi

# Construct API URL
OBP_API_URL="${OBP_BASE_URL%/}/obp/v5.1.0/users"

# Create JSON payload
read -r -d '' PAYLOAD << EOM
{
  "email": "$OBP_EMAIL",
  "username": "$OBP_USERNAME",
  "password": "$OBP_PASSWORD",
  "first_name": "$OBP_FIRST_NAME",
  "last_name": "$OBP_LAST_NAME"
}
EOM

# Send the request
echo "📡 Sending request to $OBP_API_URL..."
RESPONSE=$(curl --silent --location "$OBP_API_URL" \
  --header "Content-Type: application/json" \
  --data-raw "$PAYLOAD")

# Output response (prettified if jq is installed)
if command -v jq >/dev/null 2>&1; then
  echo "$RESPONSE" | jq .
else
  echo "$RESPONSE"
fi
