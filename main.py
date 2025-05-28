from kubernetes_api_client import KubernetesApiClient

import bootstrap_config
from create_user import create_obp_user
from create_consumer_keys import create_consumer_keys
from keycloak_import import create_client_explorer, create_client_manager
from check_api_alive import wait_for_obp_api

k8s_client = KubernetesApiClient(context=bootstrap_config.k8s_context)
api_explorer_credentials = None, None
api_manager_credentials = None, None
api_explorer_credentials_missing = True
api_manager_credentials_missing = True


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
k8s_api_explorer_client_key = k8s_client.get_secret_value(
	secret_name=bootstrap_config.obp_api_explorer_secret_name,
	namespace=bootstrap_config.obp_api_explorer_namespace,
	key='VITE_OBP_CONSUMER_KEY'
)
if k8s_api_explorer_client_key not in (None, "None", "some_value"):
	api_explorer_credentials_missing = False


k8s_api_manager_client_key = k8s_client.get_secret_value(
	secret_name=bootstrap_config.obp_api_manager_secret_name,
	namespace=bootstrap_config.obp_api_manager_namespace,
	key='VITE_OBP_CONSUMER_KEY'
)
if k8s_api_manager_client_key not in (None, "None", "some_value"):
	api_manager_credentials_missing = False

if bootstrap_config.register_with_keycloak:
	print("Registering with Keycloak is not supported yet.")
	if api_explorer_credentials_missing:
		api_explorer_credentials = create_client_explorer()
	if api_manager_credentials_missing:
		api_manager_credentials = create_client_manager()
else:
	if api_explorer_credentials_missing:
		api_explorer_credentials = create_consumer_keys("api-explorer")
	api_manager_credentials_missing:(
		api_manager_credentials) = create_consumer_keys("api-manager")


if api_explorer_credentials_missing:
	key, secret = api_explorer_credentials
	k8s_client.update_secret(
		secret_name=bootstrap_config.obp_api_explorer_secret_name,
		namespace=bootstrap_config.obp_api_explorer_namespace,
		key='VITE_OBP_CONSUMER_KEY',
		value=key
	)
	k8s_client.update_secret(
		secret_name=bootstrap_config.obp_api_explorer_secret_name,
		namespace=bootstrap_config.obp_api_explorer_namespace,
		key='VITE_OBP_CONSUMER_SECRET',
		value=secret
	)
if api_manager_credentials_missing:
	key, secret = api_manager_credentials
	k8s_client.update_secret(
		secret_name=bootstrap_config.obp_api_manager_secret_name,
		namespace=bootstrap_config.obp_api_manager_namespace,
		key='OAUTH_CONSUMER_KEY',
		value=key
	)
	k8s_client.update_secret(
		secret_name=bootstrap_config.obp_api_manager_secret_name,
		namespace=bootstrap_config.obp_api_manager_namespace,
		key='OAUTH_CONSUMER_SECRET',
		value=secret
	)


