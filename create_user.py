from test_registeruserandconsumer import TestRegisteruserandconsumer, logger
from time import sleep
import bootstrap_config
import requests
import json


def create_obp_user():
	url = f"{bootstrap_config.obp_apihost}/obp/v5.1.0/users"

	payload = json.dumps({
	  "email": bootstrap_config.obp_email,
	  "username": bootstrap_config.obp_username,
	  "password": bootstrap_config.obp_password,
	  "first_name": bootstrap_config.obp_first_name,
	  "last_name": bootstrap_config.obp_last_name,
	})
	headers = {
	  'Content-Type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	try:
		user_id = response.json().get["user_id"]
	except json.JSONDecodeError as e:
		logger.error(f"Failed to decode JSON response from user creation: {e}")
		logger.error(f"Response content: {response.content}")
		exit(1)
	except KeyError as e:
		logger.error(f"KeyError: {e} from user creation: {response.content}")
		exit(1)
	return user_id



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

# create http client

