#!/usr/bin/env python3

import atexit
import base64
import os
import requests
import time
import yaml
from pathlib import Path
from typing import Any

# NOTE: It is not recommended that most users interact with Red Hat OpenShift AI in this way. Programmatic, API-level
# access from Python code would be made much simpler by using the official Kubernetes Python client SDK:
# https://github.com/kubernetes-client/python
# Or with the OpenShift Python client, which builds on top of it with a Dynamic API:
# https://github.com/openshift/openshift-client-python
#
# If you're working in another language, chances are there's a Kubernetes SDK available for you as well.
#
# This set of examples is designed to demonstrate, in detail, how basic REST API interactions with the OpenShift AI
# APIs at the OpenShift API server could be used to provision and access OpenShift AI Workbenches, as a starting point
# to better understand API interactions with OpenShift AI in general.

# Recover the current kubeconfig to resolve a token or certificate set
kubeconfig: Path = Path(os.getenv("KUBECONFIG", None) or os.path.expanduser("~/.kube/config"))

if not kubeconfig.exists():
    raise RuntimeError(f"Unable to find kubeconfig at {kubeconfig}")

# Load the kubeconfig
with open(kubeconfig) as f:
    kubeconfig_data: dict[str, Any] = yaml.safe_load(f)

# Map the authentication in the kubeconfig
# Start by identifying the cluster, user, and current namespace

current_context: str | None = kubeconfig_data.get("current-context")
current_user: str | None = None
current_cluster: str | None = None
default_namespace: str | None = None
for context in kubeconfig_data.get("contexts", []):
    if current_context == context.get("name"):
        context_data = context.get("context", {})
        current_user = context_data.get("user")
        current_cluster = context_data.get("cluster")
        default_namespace = context_data.get("namespace")
        break
if current_user is None or current_cluster is None:
    raise RuntimeError(f"Unable to identify user or cluster from current context in kubeconfig at {kubeconfig}")

# Map to the API URL for the cluster
api_url: str | None = None
for cluster in kubeconfig_data.get("clusters", []):
    if current_cluster == cluster.get("name"):
        api_url = cluster.get("cluster", {}).get("server")
        break
if api_url is None:
    raise RuntimeError(f"Unable to identify the server URL from current context in kubeconfig at {kubeconfig}")

# Create a requests.Session object for working with the cluster
session = requests.Session()
session.headers.update({"Content-Type": "application/json"})

# Map to the user's token or certificate and key
# The following section will allow us to use the most common methods of authentication stored in the kubeconfig we identified
token: str | None = None
client_cert: str | None = None
client_key: str | None = None
maybe_authenticated: bool = False
client_cert_file = Path("/tmp/client.crt")
client_key_file = Path("/tmp/client.key")


@atexit.register
def cleanup_tmp_certs():
    """Clean up any temporarily stored certificates, if any, when the program completes."""
    if client_cert_file.exists() or client_key_file.exists():
        print("Cleaning up tempoarily stored certificates")
    client_cert_file.unlink(missing_ok=True)
    client_key_file.unlink(missing_ok=True)


for user in kubeconfig_data.get("users", []):
    if current_user == user.get("name"):
        user_data = user.get("user", {})
        token = user_data.get("token")
        if token is None:
            # Attempt to access the client certificate and key from the Kubeconfig,
            # saving them in a way that allows requests to use them
            client_cert = user_data.get("client-certificate-data")
            client_key = user_data.get("client-key-data")
            if client_cert is not None and client_key is not None:
                with open(client_cert_file, "wb") as f:
                    f.write(base64.b64decode(client_cert))
                with open(client_key_file, "wb") as f:
                    f.write(base64.b64decode(client_key))
                session.cert = (client_cert_file, client_key_file) # type: ignore
                maybe_authenticated = True
        else:
            # Use our bearer token, if saved in the Kubeconfig
            session.headers.update({"Authorization": f"Bearer {token}"})
            maybe_authenticated = True
        break

# Confirm that our requests.Session is set up correctly to interact with the API server
if maybe_authenticated:
    if session.get(f"{api_url}/api").status_code != 200:
        raise RuntimeError(f"Unable to reach server at {api_url} as {current_user}")
else:
    raise RuntimeError(f"Unable to identify authentication information from your current context in the kubeconfig at {kubeconfig}")

current_openshift_username = current_user.split("/", 1)[0]

def exists(api_namespace: str = "v1", namespace: str | None = None, resourcekind: str = "", name: str = "") -> bool:
    """Helper function to check if a resource exists."""
    if api_namespace == "v1":
        endpoint = f"api/{api_namespace}"
    else:
        endpoint = f"apis/{api_namespace}"
    if namespace is not None:
        endpoint += f"/namespaces/{namespace}"
    endpoint += f"/{resourcekind}/{name}"
    response = session.get(f"{api_url}/{endpoint}").json()
    if response.get("status") == "Failure":
        return False
    return True

def create(api_namespace: str = "v1", namespace: str | None = None, resourcekind: str = "", data: dict = {}) -> dict:
    """Helper function to create resources of different kinds,
    returning the server's JSON response as a dictionary."""
    if api_namespace == "v1":
        endpoint = f"api/{api_namespace}"
    else:
        endpoint = f"apis/{api_namespace}"
    if namespace is not None:
        endpoint += f"/namespaces/{namespace}"
    endpoint += f"/{resourcekind}"
    return session.post(f"{api_url}/{endpoint}", json=data).json()


def b64(inputstr: str) -> str:
    """Helper function to make it simpler to base64 encode Python strings, returning strings."""
    return base64.b64encode(inputstr.encode("utf8")).decode("utf8")


def route_url(namespace: str, name: str) -> str | None:
    """Helper function to retrieve the effective URL of a given Route."""
    try:
        return session.get(f"{api_url}/apis/route.openshift.io/v1/namespaces/{namespace}/routes/{name}").json().get("status", {}).get("ingress", [{}])[0].get("host")
    except Exception:
        return None


def notebook_ready(namespace: str, name: str) -> bool:
    """Helper function to identify whether a Kubeflow Notebook resource is ready."""
    try:
        return session.get(f"{api_url}/apis/kubeflow.org/v1/namespaces/{namespace}/notebooks/{name}").json().get("status", {}).get("readyReplicas", 0) > 0
    except Exception:
            return False


# Recover the Dashboard URL to inject into the Jupyter arguments to associate with our OAuth session properly
# NOTE: Also makes sure the cluster we're on has RHOAI installed (though doesn't check for the workbench controller)
dashboard_url = route_url(namespace="redhat-ods-applications", name="rhods-dashboard")
if dashboard_url is None:
    raise RuntimeError("Unable to confirm the Dashboard URL in your RHOAI installation")

# Name our resources in related and predictable ways
common_name = "api-example"
if default_namespace is None or default_namespace == "default":
    # Note that we can't use default as the operator doesn't watch Notebook resources here
    common_namespace = "api-example"
else:
    common_namespace = default_namespace

# Define a namespace
namespace = {
    "metadata": {
        "name": common_namespace,
        "labels": {
            "opendatahub.io/dashboard": "true",
        },
    },
}
if not exists(resourcekind="namespaces", name=common_namespace):
    print("Data Science Project (Namespace) being created:")
    print(yaml.dump(namespace))
    create(resourcekind="namespaces", data=namespace)
else:
    print(f"Reusing Data Science Project (Namespace): {common_namespace}")

# Define a Kubernetes Secret for use as an OpenShift AI S3 Data Connection
# NOTE: the values are not checked to be accurate except maybe by notebook code, which is not shown here
data_connection_secret = {
    "metadata": {
        "name": common_name,
        "annotations": {
            "opendatahub.io/connection-type": "s3",
        },
        "labels": {
            "opendatahub.io/dashboard": "true",
            "opendatahub.io/managed": "true",
        },
    },
    "data": {
        "AWS_ACCESS_KEY_ID": b64("minio"),
        "AWS_DEFAULT_REGION": "",
        "AWS_S3_BUCKET": "",
        "AWS_S3_ENDPOINT": b64("http://minio.minio.svc:9000"),
        "AWS_SECRET_ACCESS_KEY": b64("minio123"),
    },
}
if not exists(resourcekind="secrets", namespace=common_namespace, name=common_name):
    print(f"Data Connection (Secret) being created in {common_namespace}:")
    print(yaml.dump(data_connection_secret))
    create(resourcekind="secrets", namespace=common_namespace, data=data_connection_secret)
else:
    print(f"Reusing Data Connection (Secret) {common_name} in {common_namespace}")

# Define a Kubernetes PVC using the default StorageClass provided by the cluster, to
# serve as workbench storage for notebook code and other artifacts
workbench_pvc = {
    "metadata": {
        "name": common_name,
        "labels": {
            "opendatahub.io/dashboard": "true",
        },
    },
    "spec": {
        "accessModes": ["ReadWriteOnce"],
        "resources": {
            "requests": {
                "storage": "10Gi",
            },
        },
        "volumeMode": "Filesystem",
    },
}
if not exists(resourcekind="persistentvolumeclaims", namespace=common_namespace, name=common_name):
    print(f"Workbench Storage (PVC) being created in {common_namespace}:")
    print(yaml.dump(workbench_pvc))
    create(resourcekind="persistentvolumeclaims", namespace=common_namespace, data=workbench_pvc)
else:
    print(f"Reusing Workbench Storage (PVC) {common_name} in {common_namespace}")

# Define a Kubeflow Notebook, referred to in the OpenShift AI documentation and UI as a Workbench
# NOTE: The image used here is available in up-to-date OpenShift AI 2.15 clusters, and the resources
# allocated in this example align with the default Small workbench flavor in the UI
workbench = {
    "apiVersion": "kubeflow.org/v1", # Note that the extension APIs require the APIVersion and Kind specified in their posted data, unlike v1 APIs
    "kind": "Notebook",
    "metadata": {
        "name": common_name,
        "annotations": {
            "notebooks.opendatahub.io/inject-oauth": "true", # this will ensure we can log in to our notebook with OpenShift OAuth
            "opendatahub.io/accelerator-name": "",
            "opendatahub.io/image-display-name": "Minimal Python", # This is a friendly name that should align with a Notebook ImageStream's display name
            "opendatahub.io/username": current_openshift_username,
            "openshift.io/display-name": common_name,
        },
        "labels": {
            "app": common_name,
            "opendatahub.io/dashboard": "true",
            "opendatahub.io/odh-managed": "true",
            "opendatahub.io/user": current_openshift_username,
        },
    },
    "spec": {
        "template": {
            "spec": {
                "affinity": {},
                "containers": [
                    {
                        "env": [
                            { # The following templated strings are to wire Jupyter up to support normal RHOAI links and behavior
                              # Note, in particular, that the ServerApp.base_url aligns to our namespace and Notebook name. This is used
                              # throughout the rest of this manifest.
                                "name": "NOTEBOOK_ARGS",
                                "value": "--ServerApp.port=8888 --ServerApp.token=''"
                                         f" --ServerApp.password='' --ServerApp.base_url=/notebook/{common_namespace}/{common_name}"
                                         " --ServerApp.quit_button=False"
                                         ' --ServerApp.tornado_settings={"user":"' + current_openshift_username + '","hub_host":"https://' + dashboard_url + '","hub_prefix":"/projects/' + common_namespace + '"}',
                            },
                            {
                                "name": "JUPYTER_IMAGE",
                                "value": "image-registry.openshift-image-registry.svc:5000/redhat-ods-applications/s2i-minimal-notebook:2024.2",
                            },
                            { # All of these certificates are available in the namespace by default as they're injected by the RHOAI Operator
                                "name": "PIP_CERT",
                                "value": "/etc/pki/tls/custom-certs/ca-bundle.crt",
                            },
                            {
                                "name": "REQUESTS_CA_BUNDLE",
                                "value": "/etc/pki/tls/custom-certs/ca-bundle.crt",
                            },
                            {
                                "name": "SSL_CERT_FILE",
                                "value": "/etc/pki/tls/custom-certs/ca-bundle.crt",
                            },
                            {
                                "name": "PIPELINES_SSL_SA_CERTS",
                                "value": "/etc/pki/tls/custom-certs/ca-bundle.crt",
                            },
                            {
                                "name": "GIT_SSL_CAINFO",
                                "value": "/etc/pki/tls/custom-certs/ca-bundle.crt",
                            },
                        ],
                        "envFrom": [
                            { # This is selecting the S3 Data Connection Secret we defined above
                                "secretRef": {
                                    "name": common_name,
                                },
                            },
                        ],
                        "image": "image-registry.openshift-image-registry.svc:5000/redhat-ods-applications/s2i-minimal-notebook:2024.2",
                        "imagePullPolicy": "Always",
                        "livenessProbe": {
                            "failureThreshold": 3,
                            "httpGet": {
                                "path": f"/notebook/{common_namespace}/{common_name}/api",
                                "port": "notebook-port",
                                "scheme": "HTTP",
                            },
                            "initialDelaySeconds": 10,
                            "periodSeconds": 5,
                            "successThreshold": 1,
                            "timeoutSeconds": 1,
                        },
                        "name": common_name,
                        "ports": [
                            {
                                "containerPort": 8888,
                                "name": "notebook-port",
                                "protocol": "TCP",
                            },
                        ],
                        "readinessProbe": {
                            "failureThreshold": 3,
                            "httpGet": {
                                "path": f"/notebook/{common_namespace}/{common_name}/api",
                                "port": "notebook-port",
                                "scheme": "HTTP",
                            },
                            "initialDelaySeconds": 10,
                            "periodSeconds": 5,
                            "successThreshold": 1,
                            "timeoutSeconds": 1,
                        },
                        "resources": { # These resources align with the default Small workbench size
                            "limits": {
                                "cpu": "2",
                                "memory": "8Gi",
                            },
                            "requests": {
                                "cpu": "1",
                                "memory": "8Gi",
                            },
                        },
                        "volumeMounts": [
                            {
                                "mountPath": "/opt/app-root/src",
                                "name": common_name,
                            },
                            {
                                "mountPath": "/dev/shm",
                                "name": "shm",
                            },
                            { # This is that RHOAI-injected CA bundle - note that it's not specified in the Volumes, but it will be mutated to include this
                                "mountPath": "/etc/pki/tls/custom-certs/ca-bundle.crt",
                                "name": "trusted-ca",
                                "readOnly": True,
                                "subPath": "ca-bundle.crt",
                            },
                        ],
                        "workingDir": "/opt/app-root/src",
                    },
               ],
                "serviceAccountName": common_name, # This is created automatically in response to our Notebook resource being created
                "enableServiceLinks": False,
                "volumes": [
                    { # This is the PVC we defined above for workbench storage
                        "name": common_name,
                        "persistentVolumeClaim": {
                            "claimName": common_name,
                        },
                    },
                    { # This is commonly needed by various ML libraries
                        "emptyDir": {
                            "medium": "Memory",
                        },
                        "name": "shm",
                    },
                ],
            },
        },
    },
}
if not exists(api_namespace="kubeflow.org/v1", resourcekind="notebooks", namespace=common_namespace, name=common_name):
    print(f"Workbench (Kubeflow Notebook) being created in {common_namespace}:")
    print(yaml.dump(workbench))
    create(api_namespace="kubeflow.org/v1", resourcekind="notebooks", namespace=common_namespace, data=workbench)
    print("Waiting until ready", end="", flush=True)
    while not notebook_ready(namespace=common_namespace, name=common_name):
        print(".", end="", flush=True)
        time.sleep(1)
    print()
else:
    print(f"Reusing Workbench (Kubeflow Notebook) {common_name} in {common_namespace}")

print(f"Retrieving URL from Route named {common_name} in {common_namespace}", end="", flush=True)
while True:
    notebook_url = route_url(namespace=common_namespace, name=common_name)
    if notebook_url is None:
        print(".", end="", flush=True)
        time.sleep(1)
    else:
        break
print()

print(f"Your workbench can be accessed at: https://{notebook_url}/notebook/{common_namespace}/{common_name}")
