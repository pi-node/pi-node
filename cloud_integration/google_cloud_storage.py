# Google Cloud Storage client for storing and retrieving files
from google.cloud import storage
from google.cloud import kms

storage_client = storage.Client()
kms_client = kms.KeyManagementServiceClient()

def upload_file_to_gcs(file_path, bucket_name, encryption_key):
    # Create a GCS bucket client
    bucket = storage_client.bucket(bucket_name)

    # Encrypt the file using KMS
    encryption_key_name = f'projects/{kms_client.project}/locations/global/keyRings/my-key-ring/cryptoKeys/{encryption_key}'
    encrypted_file = encrypt_file(file_path, encryption_key_name)

    # Upload the encrypted file to GCS
    blob = bucket.blob('encrypted_file.txt')
    blob.upload_from_string(encrypted_file)

    return blob.public_url

def encrypt_file(file_path, encryption_key_name):
    # Encrypt the file using KMS
    kms_response = kms_client.encrypt(
        request={
            'name': encryption_key_name,
            'plaintext': open(file_path, 'rb').read()
        }
    )
    encrypted_data = kms_response.ciphertext

    return encrypted_data
