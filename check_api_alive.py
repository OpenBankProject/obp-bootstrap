import bootstrap_config
import requests
from time import sleep
import json


def wait_for_obp_api():
	url = f"{bootstrap_config.obp_apihost}/alive"

	while True:
		try:
			sleep(20)  # Wait for the API to be ready
			response = requests.get(url)
			if response.status_code == 200:
				return 0
			else:
				print(f"API returned status code: {response.status_code}")
		except requests.exceptions.RequestException as e:
			print(f"Error connecting to API: {e}")


