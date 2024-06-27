#!/bin/bash

# Check if sleep mode is enabled
if [ $(jq -r '.sleep_mode' /etc/pi-node/config.json) == "true" ]; then
  # Put node to sleep
  sudo systemctl suspend
fi
