from dotenv import load_dotenv
from os import getenv


load_dotenv()
k8s_context = getenv('K8S_CONTEXT')

obp_apihost = getenv('BOOTSTRAP_OBP_APIHOST')
obp_api_portalhost = getenv('BOOTSTRAP_OBP_API_PORTALHOST', obp_apihost)
obp_username = getenv('BOOTSTRAP_OBP_USERNAME')
obp_password = getenv('BOOTSTRAP_OBP_PASSWORD')
obp_user_exists = getenv('BOOTSTRAP_OBP_USER_EXISTS', 'true').lower() == 'true'
if not obp_user_exists:
	obp_first_name = getenv('BOOTSTRAP_OBP_FIRST_NAME', 'first_name')
	obp_last_name = getenv('BOOTSTRAP_OBP_LAST_NAME', 'last_name')
	k8s_obp_api_namespace = getenv('K8S_OBP_API_NAMESPACE')
	k8s_obp_api_deployment = getenv('K8S_OBP_API_DEPLOYMENT')
obp_email = getenv('BOOTSTRAP_OBP_EMAIL','admin@mydomain.kube')
app_name = getenv("APP_NAME", "api-explorer")
app_k8s_secret_name = getenv("APP_K8S_SECRET_NAME", "my-api-explorer-secret")
app_k8s_client_key_name = getenv("APP_K8S_SECRET_KEY_NAME", "VITE_OBP_CONSUMER_KEY")
app_k8s_client_secret_name = getenv("APP_K8S_CLIENT_SECRET_NAME", "VITE_OBP_CONSUMER_SECRET")
app_namespace = getenv("APP_NAMESPACE", "obp")
app_hostname = getenv("APP_HOSTNAME", "api-explorer.mydomain.kube")
register_with_keycloak = getenv("REGISTER_WITH_KEYCLOAK", "false").lower() == "true"
if register_with_keycloak:
	keycloak_server = getenv("KEYCLOAK_SERVER")
	if keycloak_server is None:
		raise RuntimeError("Environment variable 'KEYCLOAK_SERVER' is required but not set.")
	keycloak_username = getenv("KEYCLOAK_USERNAME")
	if keycloak_username is None:
		raise RuntimeError("Environment variable 'KEYCLOAK_USERNAME' is required but not set.")
	keycloak_password = getenv("KEYCLOAK_PASSWORD")
	if keycloak_password is None:
		raise RuntimeError("Environment variable 'KEYCLOAK_PASSWORD' is required but not set.")
	keycloak_realm = getenv("KEYCLOAK_REALM")
	if keycloak_realm is None:
		raise RuntimeError("Environment variable 'KEYCLOAK_REALM' is required but not set.")
