import bootstrap_config
import requests
from create_consumer_keys_api import create_obp_consumer_keys
from keycloak import KeycloakAdmin, KeycloakOpenID


keycloak_admin = KeycloakAdmin(
    server_url=bootstrap_config.keycloak_server,
    username=bootstrap_config.keycloak_username,
    password=bootstrap_config.keycloak_password,
    realm_name=bootstrap_config.keycloak_realm,
    verify=True
)

client_representation_app = {
    "id": bootstrap_config.keycloak_deploy_client_id,
    "name": bootstrap_config.keycloak_deploy_client_id,
    "clientId": bootstrap_config.keycloak_deploy_client_id,
    "enabled": True,
    "publicClient": False,  # Require client secret
    "serviceAccountsEnabled": True,  # Enable service account
    "authorizationServicesEnabled": True,  # Enable authorization
    "redirectUris": [f"{bootstrap_config.app_hostname}/main/"]
}


def get_or_create_can_create_consumer_role():
    roles = keycloak_admin.get_realm_roles()
    if not any(role['name'] == "CanCreateConsumer" for role in roles):
        keycloak_admin.create_realm_role({"name": "CanCreateConsumer"})
        print("Realm role 'CanCreateConsumer' created.")
    else:
        print("Realm role 'CanCreateConsumer' already exists.")


def get_client_uuid(client_id):
    clients = keycloak_admin.get_clients()
    for client in clients:
        if client['clientId'] == client_id:
            return client['id']
    raise Exception(f"Client with clientId {client_id} not found.")

def get_or_create_client_role(client_id, role_name):
    client_uuid = get_client_uuid(client_id)
    try:
        role = keycloak_admin.get_client_role(client_id=client_uuid, role_name=role_name)
    except Exception:
        keycloak_admin.create_client_role(client_role_id=client_uuid, payload={"name": role_name})
        role = keycloak_admin.get_client_role(client_id=client_uuid, role_name=role_name)
    return role

def assign_can_create_consumer_role_to_service_account(client_id, role):
    client_uuid = get_client_uuid(client_id)
    service_account_user = keycloak_admin.get_client_service_account_user(client_uuid)
    service_account_user_id = service_account_user['id']
    keycloak_admin.assign_client_role(user_id=service_account_user_id, client_id=client_uuid, roles=[role])
    print(f"Assigned 'CanCreateConsumer' client role to service account user: {service_account_user_id}.")

def create_keycloak_client():
    client_response = keycloak_admin.create_client(client_representation_app)
    print(client_response)

    client_id = bootstrap_config.keycloak_deploy_client_id
    print(client_id)
    print(keycloak_admin.get_client_secrets(client_id))
    client_secret = keycloak_admin.get_client_secrets(client_id)["value"]
    return client_id, client_secret


def create_openid_token(client_id, client_secret):
    keycloak_openid = KeycloakOpenID(
        server_url=bootstrap_config.keycloak_server,
        client_id=client_id,
        realm_name=bootstrap_config.keycloak_realm,
        client_secret_key=client_secret
    )
    token = keycloak_openid.token(grant_type='client_credentials')
    return token['access_token']


def bootstrap_bearer_token():
    client_id, client_secret = create_keycloak_client()
    client_id = bootstrap_config.keycloak_deploy_client_id
    role = get_or_create_client_role(client_id, "CanCreateConsumer")
    print(f"Role: {role}")
    try:
        assign_role = assign_can_create_consumer_role_to_service_account(client_id, role)
        print(f"Assigned role: {assign_role}")
    except Exception as e:
        print(f"Error assigning role: {e}, ignoring for now")
    #assign_can_create_consumer_role_to_service_account(client_id, role)
    bearer_token = create_openid_token(client_id, client_secret)
    return bearer_token


def get_current_obp_user(token):
    url = f"{bootstrap_config.obp_apihost}/obp/v5.1.0/users/current"
    headers = {
	  'Authorization': f'Bearer {token}',
	}
    response = requests.request("GET", url, headers=headers)
    return response.json()
