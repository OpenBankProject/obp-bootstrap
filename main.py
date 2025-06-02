from kubernetes_api_client import KubernetesApiClient

import bootstrap_config
from create_user import create_obp_user
from create_consumer_keys import create_consumer_keys
from check_api_alive import wait_for_obp_api

k8s_client = KubernetesApiClient(context=bootstrap_config.k8s_context)
app_credentials = None, None
app_credentials_missing = True


wait_for_obp_api()
if not bootstrap_config.obp_user_exists:
	api_skips_email_validation = k8s_client.get_env_value(
		bootstrap_config.k8s_obp_api_deployment,
		bootstrap_config.k8s_namespace,
		'OBP_AUTHUSER_SKIPEMAILVALIDATION').lower() == 'true'
	if not api_skips_email_validation:
		raise RuntimeError(
			"""Environment variable 'OBP_AUTHUSER_SKIPEMAILVALIDATION' needs to be set to 'true'
			 to create a valid user. Plz set accordingly. 
			 You might want to ensure that the api is not exposed to the internet at that point.""")
	user_id = create_obp_user()
	print(f"Created user with user_id: {user_id}")

# Check if the API Explorer and API Manager consumer keys exist in Kubernetes secrets
k8s_app_client_key = k8s_client.get_secret_value(
	secret_name=bootstrap_config.app_k8s_secret_name,
	namespace=bootstrap_config.app_namespace,
	key=bootstrap_config.app_k8s_client_key_name
)
if k8s_app_client_key not in (None, "None", "some_value"):
	app_credentials_missing = False
if app_credentials_missing:
	print("No consumer keys found in Kubernetes secrets, creating new ones...")
	if bootstrap_config.register_with_keycloak:
		# Apps do not support keycloak registration yet.
		from keycloak_import import create_app_client
		print("Registering with Keycloak is not supported yet.")
		app_credentials = create_app_client()

	else:
			app_credentials = create_consumer_keys()
	key, secret = app_credentials
	update_key = k8s_client.update_secret(
		secret_name=bootstrap_config.app_k8s_secret_name,
		namespace=bootstrap_config.app_namespace,
		key=bootstrap_config.app_k8s_client_key_name,
		value=key
	)
	k8s_client.update_secret(
		secret_name=bootstrap_config.app_k8s_secret_name,
		namespace=bootstrap_config.app_namespace,
		key=bootstrap_config.app_k8s_client_secret_name,
		value=secret
	)



