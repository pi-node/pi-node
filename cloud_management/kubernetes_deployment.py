# Kubernetes client for managing containerized applications
from kubernetes import client, config

config.load_kube_config()

def create_deployment(namespace, deployment_name, container_image):
    """
    Create a new deployment
    """
    api_client = client.ApiClient()
    deployment = client.V1Deployment()
    deployment.metadata = client.V1ObjectMeta(name=deployment_name)
    deployment.spec = client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(match_labels={'app': deployment_name}),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={'app': deployment_name}),
            spec=client.V1PodSpec(containers=[client.V1Container(name=deployment_name, image=container_image)])
        )
    )
    response = api_client.create_namespaced_deployment(namespace, deployment)
    return response

def update_deployment(namespace, deployment_name,container_image):
    """
    Update an existing deployment
    """
    api_client = client.ApiClient()
    deployment = api_client.get_namespaced_deployment(namespace, deployment_name)
    deployment.spec.template.spec.containers[0].image = container_image
    response = api_client.patch_namespaced_deployment(namespace, deployment_name, deployment)
    return response

def delete_deployment(namespace, deployment_name):
    """
    Delete a deployment
    """
    api_client = client.ApiClient()
    response = api_client.delete_namespaced_deployment(namespace, deployment_name)
    return response

def get_deployment(namespace, deployment_name):
    """
    Get a deployment
    """
    api_client = client.ApiClient()
    response = api_client.get_namespaced_deployment(namespace, deployment_name)
    return response
