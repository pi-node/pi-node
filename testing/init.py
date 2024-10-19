import logging
import importlib
from pathlib import Path

# Configure logging
logging.basicConfig(filename='pi_supernode.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def discover_packages():
    """Automatically discover packages in the current directory."""
    logging.info("Discovering packages.")
    packages = []
    for path in Path('.').rglob('*.py'):
        if path.parent.name != '__pycache__':
            package_name = path.parent.name
            if package_name not in packages:
                packages.append(package_name)
    return packages

def load_packages(packages):
    """Load the discovered packages."""
    logging.info("Loading packages.")
    for package in packages:
        try:
            importlib.import_module(package)
            logging.info(f"Loaded package: {package}")
        except ImportError as e:
            logging.error(f"Failed to load package: {package}\nError: {e}")

def main():
    """Main entry point for the Pi Supernode application."""
    logging.info("Starting Pi Supernode application.")
    packages = discover_packages()
    load_packages(packages)

if __name__ == "__main__":
    main()
