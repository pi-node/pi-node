import requests

# Kusama API endpoint
KUSAMA_API = 'https://kusama.network/api'

# Get node information from Kusama API
def get_node_info():
    response = requests.get(KUSAMA_API + '/nodes')
    return response.json()

# Send transaction to Kusama network
def send_transaction(tx_data):
    response = requests.post(KUSAMA_API + '/transactions', json=tx_data)
    return response.json()
