import asyncio
import json
from typing import Dict, List

class NodeScheduler:
    def __init__(self, nodes: List[Dict[str, str]]):
        self.nodes = nodes
        self.tasks = {}

    async def schedule_task(self, task_id: str, node_id: str) -> None:
        node = next((node for node in self.nodes if node['id'] == node_id), None)
        if node:
            self.tasks[task_id] = node
            print(f"Scheduled task {task_id} on node {node_id}")
        else:
            print(f"Node {node_id} not found")

    async def get_task_status(self, task_id: str) -> str:
        node = self.tasks.get(task_id)
        if node:
            return f"Task {task_id} is running on node {node['id']}"
        else:
            return f"Task {task_id} not found"

    async def cancel_task(self, task_id: str) -> None:
        node = self.tasks.pop(task_id, None)
        if node:
            print(f"Cancelled task {task_id} on node {node['id']}")
        else:
            print(f"Task {task_id} not found")

async def main():
    nodes = [
        {'id': 'node1', 'ip': '192.168.1.100', 'port': 8080},
        {'id': 'node2', 'ip': '192.168.1.101', 'port': 8080},
        {'id': 'node3', 'ip': '192.168.1.102', 'port': 8080},
    ]
    scheduler = NodeScheduler(nodes)

    await scheduler.schedule_task('task1', 'node1')
    await scheduler.schedule_task('task2', 'node2')
    await scheduler.schedule_task('task3', 'node3')

    print(await scheduler.get_task_status('task1'))
    print(await scheduler.get_task_status('task2'))
    print(await scheduler.get_task_status('task3'))

    await scheduler.cancel_task('task2')
    print(await scheduler.get_task_status('task2'))

asyncio.run(main())
