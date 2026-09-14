import os
import time
from prometheus_client import start_http_server, Gauge

# Prometheus metrics
NODE_SYNC_STATUS = Gauge('node_sync_status', 'Node sync status')
NODE_PEER_COUNT = Gauge('node_peer_count', 'Node peer count')

# Start Prometheus server
start_http_server(8000)

while True:
    # Update node sync status metric
    NODE_SYNC_STATUS.set(get_sync_status())

    # Update node peer count metric
    NODE_PEER_COUNT.set(len(get_peers()))

    time.sleep(10)
