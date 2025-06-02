# obp-bootstrap
OBP deployment automation script

# Creating Consumer Keys

The script will only create consumer keys if 'VITE_OBP_CONSUMER_KEY' (api explorer) or 'OAUTH_CONSUMER_KEY' api manager) are:
- either not set
- set to 'None' or 'some_value'
