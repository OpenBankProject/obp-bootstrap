from test_registeruserandconsumer import TestRegisteruserandconsumer, logger
from time import sleep
import bootstrap_config

def create_consumer_keys(app_name):
	client = TestRegisteruserandconsumer()
	##client.use_firefox()
	sleep(3)
	auth_key = None
	auth_secret = None
	client.login(bootstrap_config.obp_apihost, bootstrap_config.obp_username, bootstrap_config.obp_password)
	try:
		auth_key, auth_secret = client.register_consumer(
			bootstrap_config.obp_apihost,
			app_name,
			bootstrap_config.obp_email,
			"bootstrap initialization",
			"bootstrap initialization"
		)
	except Exception as e:
		logger.error(f'Could not register consumer key: {e}')
	finally:
		client.teardown_method()
	return auth_key, auth_secret