# Azure Resource Manager client for managing infrastructure resources
from azure.mgmt.resource import ResourceManagementClient

resource_client = ResourceManagementClient(credential, subscription_id)

def create_resource_group(resource_group_name, location):
    """
    Create a new resource group
    """
    response = resource_client.resource_groups.create_or_update(
        resource_group_name,
        {
            'location': location
        }
    )
    return response

def create_resource(resource_group_name, resource_name, resource_type, location):
    """
    Create a new resource
    """
    response = resource_client.resources.create_or_update(
        resource_group_name,
        resource_name,
        {
            'resource_type': resource_type,
            'location': location
        }
    )
    return response

def delete_resource(resource_group_name, resource_name):
    """
    Delete a resource
    """
    response = resource_client.resources.delete(
        resource_group_name,
        resource_name
    )
    return response

def get_resource_group_resources(resource_group_name):
    """
    Get the resources associated with a resource group
    """
    response = resource_client.resources.list(
        resource_group_name
    )
    return response
