
from test_registeruserandconsumer import TestRegisteruserandconsumer, logger
from time import sleep
import bootstrap_config
import requests
import json
import uuid

def create_obp_consumer_keys(token=None):
	url = f"{bootstrap_config.obp_apihost}/obp/v5.1.0/management/consumers"

	payload = json.dumps({
  "app_name": "Test",
  "app_type": "Test",
  "description": "Description",
  "developer_email": "some@email.com",
  "company": "company",
  "redirect_url": "redirecturl",
  "created_by_user_id": "Donald Trump",
  "enabled": True,
  "created": "1014-06-05T14:33:37Z",
  "client_certificate": None,
  "logo_url": "logoUrl"
})
	headers = {
		'Content-Type': 'application/json',
		'Authorization': f'Bearer {token}'
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	try:
		result = response.json()
		print(f"Response: {result}")
	except json.JSONDecodeError as e:
		logger.error(f"Failed to decode JSON response from user creation: {e}")
		logger.error(f"Response content: {response.content}")
		exit(1)
	except KeyError as e:
		logger.error(f"KeyError: {e} from user creation: {response.content}")
		exit(1)
	return result["consumer_key"], result["consumer_secret"]



def create_obp_user_landing_page():
	client = TestRegisteruserandconsumer()
	client.use_firefox()
	sleep(3)
	try:
		client.registeruser(
			bootstrap_config.obp_apihost,
			bootstrap_config.obp_username,
			bootstrap_config.obp_password,
			bootstrap_config.obp_first_name,
			bootstrap_config.obp_last_name,
			bootstrap_config.obp_email)
	except Exception as e:
		logger.error(f"could not register the user: {e}")
	finally:
		client.teardown_method()

