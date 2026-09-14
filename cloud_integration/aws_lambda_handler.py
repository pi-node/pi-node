# AWS Lambda handler for processing IoT device data
import boto3
import json

lambda_client = boto3.client('lambda')
iot_data_client = boto3.client('iot-data')

def lambda_handler(event, context):
    # Extract device data from event
    device_id = event['device_id']
    data = event['data']

    # Process device data using AWS IoT Analytics
    analytics_client = boto3.client('iotanalytics')
    dataset_id = 'y_dataset'
    analytics_client.batch_put_message(
        datasetId=dataset_id,
        messages=[
            {
                'essageId': device_id,
                'payload': json.dumps(data)
            }
        ]
    )

    # Store processed data in Amazon S3
    s3_client = boto3.client('s3')
    bucket_name = 'y-bucket'
    s3_client.put_object(Body=json.dumps(data), Bucket=bucket_name, Key=f'{device_id}/data.json')

    return {
        'tatusCode': 200,
        'tatusMessage': 'Data processed successfully'
    }
