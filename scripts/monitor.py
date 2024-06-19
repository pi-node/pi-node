import psutil

def monitor_node():
    # Get node CPU usage
    cpu_usage = psutil.cpu_percent()

    # Get node memory usage
    mem_usage = psutil.virtual_memory().percent

    # Print node usage
    print(f"CPU usage: {cpu_usage}%")
    print(f"Memory usage: {mem_usage}%")

if __name__ == "__main__":
    monitor_node()
