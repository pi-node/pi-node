#!/bin/bash

# Check if Wake-on-LAN is enabled
if [ $(jq -r '.wake_on_lan' /etc/pi-node/config.json) == "true" ]; then
  # Send Wake-on-LAN packet
  sudo etherwake -i eth0 00:11:22:33:44:55
fi
