#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to print messages
function print_message {
    echo "=============================="
    echo "$1"
    echo "=============================="
}

# Function to check if the application is running
function check_application {
    if pgrep -f "node src/index.js" > /dev/null; then
        print_message "Application is running."
    else
        print_message "Application is not running. Starting the application..."
        nohup node src/index.js > logs/app.log 2>&1 &
        print_message "Application started."
    fi
}

# Function to monitor logs
function monitor_logs {
    print_message "Monitoring application logs..."
    tail -f logs/app.log
}

# Function to check system resource usage
function check_resources {
    print_message "Checking system resource usage..."
    echo "CPU and Memory Usage:"
    top -b -n 1 | head -n 10
}

# Main monitoring loop
function main {
    print_message "Starting monitoring script..."

    # Check if logs directory exists, if not create it
    mkdir -p logs

    # Check application status
    check_application

    # Monitor logs in the background
    monitor_logs &

    # Check system resources every 60 seconds
    while true; do
        check_resources
        sleep 60
    done
}

# Run the main function
main
