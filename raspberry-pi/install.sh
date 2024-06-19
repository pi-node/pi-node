#!/bin/bash

# Install dependencies
sudo apt update && sudo apt install -y python3 python3-pip

# Install Pi Node software
sudo pip3 install pi-node

# Configure Pi Node
sudo tee /etc/pi-node/config.json <<EOF
{
  "node_id": "node-1",
  "node_name": "Raspberry Pi Node 1",
  "sleep_mode": true,
  "wake_on_lan": true
}
EOF

# Enable Pi Node service
sudo systemctl enable pi-node

# Start Pi Node service
sudo systemctl start pi-node
