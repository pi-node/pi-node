#!/bin/bash

# Set backup variables
BACKUP_DIR="/backup"
NODE_DATA_DIR="/var/lib/pi-supernode"

# Create backup directory
sudo mkdir -p $BACKUP_DIR

# Backup node data
sudo rsync -avz $NODE_DATA_DIR $BACKUP_DIR

# Create recovery script
sudo tee /usr/local/bin/recover_node <<EOF
#!/bin/bash
sudo rsync -avz $BACKUP_DIR $NODE_DATA_DIR
sudo systemctl restart pi-supernode
EOF

# Make recovery script executable
sudo chmod +x /usr/local/bin/recover_node
