# obp-bootstrap
OBP deployment automation script.

Running host/image needs chrome installed and the chromedriver executable available in the PATH.

### Authenticating to K8s
If run locally, the script will use your local kubeconfig file to authenticate to the Kubernetes cluster.

Running in the cluster, it will look for "/var/run/secrets/kubernetes.io/serviceaccount/token".

### Creating OBP User
The script will assume that the OBP user is already created. If you want to create a new OBP user, set BOOTSTRAP_OBP_USER_EXISTS to false
If you have not turned e-mail validation off (setting OBP_AUTHUSER_SKIPEMAILVALIDATION to true) on api side script will fail.
### Creating Consumer Keys
Done via the OBP Portal Page through Selenium webdriver by default, or via keycloak bearer token. 

#### Creating Consumer Keys using the Portal Page
Running host/image needs chrome installed and the chromedriver executable available in the PATH.

#### Creating Consumer Keys via OBP API with Keycloak bearer token

OBP API needs to allow role assignment via bearer token: Set OBP_OAUTH2_KEYCLOAK_RESOURCE_ACCESS_KEY_NAME_TO_TRUST at OBP configuration/
Set REGISTER_WITH_KEYCLOAK = "true" if you want to register consumer keys via obp api with keycloak bearer token.
KEYCLOAK_DEPLOY_CLIENT_ID needs to be the same as configured in OBP_OAUTH2_KEYCLOAK_RESOURCE_ACCESS_KEY_NAME_TO_TRUST


The script will read the existing consumer key pair from the k8s secret objects of the running api explorer and api manager deployments.

It will only create consumer keys if 'VITE_OBP_CONSUMER_KEY' (api explorer) or 'OAUTH_CONSUMER_KEY' api manager) are:
- either not set
- set to 'None' or 'some_value'
in the k8s secret objects of the running deployments.

The created consumer keys will be patched into the k8s secret objects of the running api explorer and api manager deployments.
