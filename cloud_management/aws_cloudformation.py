# AWS CloudFormation client for managing infrastructure resources
import boto3

cloudformation_client = boto3.client('cloudformation')

def create_stack(stack_name, template_body):
    """
    Create a new CloudFormation stack
    """
    response = cloudformation_client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body
    )
    return response

def update_stack(stack_name, template_body):
    """
    Update an existing CloudFormation stack
    """
    response = cloudformation_client.update_stack(
        StackName=stack_name,
        TemplateBody=template_body
    )
    return response

def delete_stack(stack_name):
    """
    Delete a CloudFormation stack
    """
    response = cloudformation_client.delete_stack(
        StackName=stack_name
    )
    return response

def get_stack_resources(stack_name):
    """
    Get the resources associated with a CloudFormation stack
    """
    response = cloudformation_client.describe_stack_resources(
        StackName=stack_name
    )
    return response

def get_stack_events(stack_name):
    """
    Get the events associated with a CloudFormation stack
    """
    response = cloudformation_client.describe_stack_events(
        StackName=stack_name
    )
    return response
