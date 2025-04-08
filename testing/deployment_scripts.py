import os
import subprocess
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='deployment.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Command executed successfully: {command}")
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command: {command}\nError: {e.stderr.decode('utf-8')}")
        raise

def clone_repository(repo_url, target_dir):
    """Clone the repository from the given URL."""
    if not os.path.exists(target_dir):
        logging.info(f"Cloning repository from {repo_url} to {target_dir}")
        run_command(f"git clone {repo_url} {target_dir}")
    else:
        logging.info(f"Repository already exists at {target_dir}")

def install_dependencies(target_dir):
    """Install the required dependencies using npm."""
    logging.info(f"Installing dependencies in {target_dir}")
    run_command(f"cd {target_dir} && npm install")

def start_application(target_dir):
    """Start the Node.js application."""
    logging.info(f"Starting application in {target_dir}")
    run_command(f"cd {target_dir} && npm start")

def deploy(repo_url, target_dir):
    """Deploy the application."""
    try:
        clone_repository(repo_url, target_dir)
        install_dependencies(target_dir)
        start_application(target_dir)
        logging.info("Deployment completed successfully.")
    except Exception as e:
        logging.error(f"Deployment failed: {e}")

if __name__ == "__main__":
    REPO_URL = "https://github.com/KOSASIH/pi-supernode"
    TARGET_DIR = "/path/to/your/target/directory"  # Update this path as needed

    logging.info("Deployment script started.")
    deploy(REPO_URL, TARGET_DIR)
