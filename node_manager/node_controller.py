# node_controller.py
import os
import subprocess

class NodeController:
    def __init__(self, node_id: str):
        self.node_id = node_id

    def start_node(self) -> None:
        subprocess.run(['sudo', 'systemctl', 'start', f'node-{self.node_id}.service'])

    def stop_node(self) -> None:
        subprocess.run(['sudo', 'systemctl', 'stop', f'node-{self.node_id}.service'])

    def restart_node(self) -> None:
        subprocess.run(['sudo', 'systemctl', 'restart', f'node-{self.node_id}.service'])

    def deploy_node(self, node_image: str) -> None:
        subprocess.run(['sudo', 'docker', 'run', '-d', '--name', f'node-{self.node_id}', node_image])

    def undeploy_node(self) -> None:
        subprocess.run(['sudo', 'docker', 'rm', '-f', f'node-{self.node_id}'])
