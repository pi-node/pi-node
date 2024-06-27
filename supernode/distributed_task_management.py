# distributed_task_management.py
import dask
from dask.distributed import Client

class TaskManager:
    def __init__(self):
        self.client = Client()

    def submit_task(self, task_function, *args, **kwargs):
        # Submit a task to the distributed cluster
        future = self.client.submit(task_function, *args, **kwargs)
        return future

    def get_task_result(self, future):
        # Get the result of a completed task
        return future.result()

def task_function(x, y):
    # Example task function that performs some computation
    return x + y

task_manager = TaskManager()

# Submit a task to the distributed cluster
future = task_manager.submit_task(task_function, 2, 3)

# Get the result of the task
result = task_manager.get_task_result(future)
print(f"Task result: {result}")
