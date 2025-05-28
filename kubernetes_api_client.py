import os

from kubernetes import client, config
import base64
from datetime import datetime
from kubernetes.client import AppsV1Api


class KubernetesApiClient:

    def __init__(self, context=None):
        if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/token"):
            print("Running inside Kubernetes – loading in-cluster config")
            config.load_incluster_config()
        else:
            print("Running outside Kubernetes – loading local kubeconfig")
            config.load_kube_config(context=context)

        self.core_api_client = client.CoreV1Api()
        self.apps_api_client = AppsV1Api()

    def get_namespaces(self):
        # List all namespaces
        namespaces = self.core_api_client.list_namespace()
        return namespaces.items

    def get_secret_value(self, secret_name, namespace, key):
        secret = self.core_api_client.read_namespaced_secret(name=secret_name, namespace=namespace)
        if key in secret.data:
            return base64.b64decode(secret.data[key]).decode()
        else:
            return None

    def update_secret(self, secret_name, namespace, key, value):
        # Get the secret
        secret = self.core_api_client.read_namespaced_secret(name=secret_name, namespace=namespace)

        # Update the value
        secret.data[key] = base64.b64encode(value.encode()).decode()

        # Patch the secret
        self.core_api_client.patch_namespaced_secret(name=secret_name, namespace=namespace, body=secret)

    def restart_deployment(self, deployment_name, namespace):
        # Get the deployment
        deployment = self.apps_api_client.read_namespaced_deployment(name=deployment_name, namespace=namespace)

        # Update the deployment's pod template with the current timestamp
        if deployment.spec.template.metadata.annotations is None:
            deployment.spec.template.metadata.annotations = {}
        deployment.spec.template.metadata.annotations['kubectl.kubernetes.io/restartedAt'] = datetime.now().isoformat()

        # Update the deployment
        self.apps_api_client.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)

    def get_env_value(self, deployment_name, namespace, env_key):
        deployment = self.apps_api_client.read_namespaced_deployment(deployment_name, namespace)

        # Get the environment variables of the first container
        env_vars = deployment.spec.template.spec.containers[0].env

        # Define the environment variable key to look for

        # Find and print the value of the environment variable
        for env_var in env_vars:
            if env_var.name == env_key:
                return env_var.value
            else:
                return False