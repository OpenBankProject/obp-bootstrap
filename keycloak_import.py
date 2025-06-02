import bootstrap_config
from keycloak import KeycloakAdmin


keycloak_admin = KeycloakAdmin(
    server_url=bootstrap_config.keycloak_server,
    username=bootstrap_config.keycloak_username,
    password=bootstrap_config.keycloak_password,
    realm_name=bootstrap_config.keycloak_realm,
    verify=True
)

client_representation_app = {
    "name": bootstrap_config.app_name,
    "enabled": True,
    "publicClient": True,
    "redirectUris": [f"{bootstrap_config.app_hostname}/main/"],
}


def create_app_client():
    client_id = keycloak_admin.create_client(client_representation_app)
    client_secret = keycloak_admin.get_client_secrets(client_id)["value"]
    return client_id, client_secret

