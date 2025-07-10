# access_control.py
import os
import json
from typing import Dict, List

class AccessControl:
    def __init__(self, access_control_file: str = 'access_control.json'):
        self.access_control_file = access_control_file
        self.access_control: Dict[str, List[str]] = self.load_access_control()

    def load_access_control(self) -> Dict[str, List[str]]:
        if os.path.exists(self.access_control_file):
            with open(self.access_control_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_access_control(self) -> None:
        with open(self.access_control_file, 'w') as f:
            json.dump(self.access_control, f, indent=4)

    def add_user(self, username: str, permissions: List[str]) -> None:
        self.access_control[username] = permissions
        self.save_access_control()

    def remove_user(self, username: str) -> None:
        if username in self.access_control:
            del self.access_control[username]
            self.save_access_control()

    def check_permission(self, username: str, permission: str) -> bool:
        if username in self.access_control:
            return permission in self.access_control[username]
        else:
            return False
