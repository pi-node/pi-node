# Google Cloud Deployment Manager client for managing infrastructure resources
from googleapiclient.discovery import build

deployment_manager_client = build('deploymentmanager', 'v2')

def create_deployment(project_id, deployment_name, config):
    """
    Create a new deployment
    """
    response = deployment_manager_client.deployments().insert(
        project=project_id,
        body={
            'name': deployment_name,
            'config': config
        }
    ).execute()
    return response

def update_deployment(project_id, deployment_name, config):
    """
    Update an existing deployment
    """
    response = deployment_manager_client.deployments().patch(
        project=project_id,
        deployment=deployment_name,
        body={
            'config': config
        }
    ).execute()
    return response

def delete_deployment(project_id, deployment_name):
    """
    Delete a deployment
    """
    response = deployment_manager_client.deployments().delete(
        project=project_id,
        deployment=deployment_name
    ).execute()
    return response

def get_deployment_resources(project_id, deployment_name):
    """
    Get the resources associated with a deployment
    """
    response = deployment_manager_client.resources().list(
        project=project_id,
        deployment=deployment_name
    ).execute()
    return response
