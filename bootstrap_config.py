from dotenv import load_dotenv
from os import getenv


load_dotenv()
k8s_context = getenv('K8S_CONTEXT')
k8s_namespace = getenv('K8S_NAMESPACE')
k8s_obp_api_deployment = getenv('K8S_OBP_API_DEPLOYMENT')
obp_apihost = getenv('BOOTSTRAP_OBP_APIHOST')
obp_username = getenv('BOOTSTRAP_OBP_USERNAME')
obp_password = getenv('BOOTSTRAP_OBP_PASSWORD')
obp_user_exists = getenv('BOOTSTRAP_OBP_USER_EXISTS', 'true').lower() == 'true'
if not obp_user_exists:
	obp_first_name = getenv('BOOTSTRAP_OBP_FIRST_NAME', 'first_name')
	obp_last_name = getenv('BOOTSTRAP_OBP_LAST_NAME', 'last_name')
	obp_email = getenv('BOOTSTRAP_OBP_EMAIL','admin@openbankproject.kube')
obp_api_explorer_secret_name = getenv("OBP_API_EXPLORER_SECRET_NAME", "api-explorer")
obp_api_explorer_namespace = getenv("OBP_API_EXPLORER_NAMESPACE", "obp")
obp_api_explorer_hostname = getenv("OBP_API_EXPLORER_HOSTNAME", "api-explorer.openbankproject.kube")
obp_api_manager_secret_name = getenv("OBP_API_MANAGER_SECRET_NAME", "api-manager")
obp_api_manager_namespace = getenv("OBP_API_MANAGER_NAMESPACE", "obp")
obp_api_manager_hostname = getenv("OBP_API_MANAGER_HOSTNAME", "api-manager.openbankproject.kube")
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
