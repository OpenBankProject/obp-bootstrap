import bootstrap_config
from keycloak import KeycloakAdmin

# Configuration


# Connect to Keycloak Admin
keycloak_admin = KeycloakAdmin(
    server_url=bootstrap_config.keycloak_server,
    username=bootstrap_config.keycloak_username,
    password=bootstrap_config.keycloak_password,
    realm_name=bootstrap_config.keycloak_realm,  # Admin login is usually in 'master'
    verify=True
)

# Define new client
client_representation_api_explorer = {
    "name": "api-explorer",
    "enabled": True,
    "publicClient": True,
    "redirectUris": [f"{bootstrap_config.obp_api_explorer_hostname}/main/"],
}
client_representation_api_manager = {
    "name": "api-manager",
    "enabled": True,
    "publicClient": False,
    "redirectUris": [bootstrap_config.obp_api_manager_hostname],
}

# Create client in 'myrealm'
def create_client_explorer():
    client_id = keycloak_admin.create_client(client_representation_api_explorer)
    client_secret = keycloak_admin.get_client_secrets(client_id)["value"]
    return client_id, client_secret

def create_client_manager():
    client_id = keycloak_admin.create_client(client_representation_api_manager)
    client_secret = keycloak_admin.get_client_secrets(client_id)["value"]
    return client_id, client_secret
