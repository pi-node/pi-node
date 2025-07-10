#!/bin/bash

# Set deployment variables
NODE_NAME="My Supernode"
NODE_TYPE="validator"
NETWORK_ID="kusama"
RPC_PORT=9933
WS_PORT=9944

# Install dependencies
sudo apt-get update && sudo apt-get install -y ansible

# Deploy node using Ansible
ansible-playbook -i inventory.ini deploy.yml

# Configure node
sudo tee /etc/pi-supernode/config.json <<EOF
{
  "node_name": "$NODE_NAME",
  "node_type": "$NODE_TYPE",
  "network_id": "$NETWORK_ID",
  "rpc_port": $RPC_PORT,
  "ws_port": $WS_PORT
}
EOF

# Start node service
sudo systemctl start pi-supernode
