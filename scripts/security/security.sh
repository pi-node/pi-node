#!/bin/bash

# Set security variables
FIREWALL_RULES="allow incoming traffic on port 9933 and 9944"
SSH_KEY="my_ssh_key"

# Configure firewall
sudo ufw allow $FIREWALL_RULES

# Configure SSH key
sudo mkdir -p ~/.ssh
sudo tee ~/.ssh/authorized_keys <<EOF
$SSH_KEY
EOF

# Enable automatic security updates
sudo apt-get update && sudo apt-get install -y unattended-upgrades
