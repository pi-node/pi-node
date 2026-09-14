cmake_minimum_required(VERSION 3.10)
project(PiSupernode)

# Find Python
find_package(PythonInterp 3 REQUIRED)
find_package(PythonLibs 3 REQUIRED)

# Set Python executable and libraries
set(PYTHON_EXECUTABLE ${PYTHON_EXECUTABLE})
set(PYTHON_LIBRARIES ${PYTHON_LIBRARIES})

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

# Add source files
set(SOURCE_FILES
    src/main.py
    src/config.py
    src/blockchain.py
    src/transaction.py
    src/node.py
    src/consensus.py
    src/smart_contracts.py
    src/wallet.py
    src/api.py
    src/utils.py
)

# Enable testing
enable_testing()

# Add a custom command to run tests
add_custom_target(run_tests
    COMMAND ${PYTHON_EXECUTABLE} -m pytest tests
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS ${SOURCE_FILES}
)

# Install dependencies from requirements.txt
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt")
    execute_process(COMMAND ${PYTHON_EXECUTABLE} -m pip install -r ${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt)
endif()

# Add a target for running the application
add_custom_target(run
    COMMAND ${PYTHON_EXECUTABLE} src/main.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

# Optionally, add a target for building a Docker image
add_custom_target(docker_build
    COMMAND docker build -t pi-supernode .
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

# Set the default target to run the application
set_property(DIRECTORY PROPERTY ADDITIONAL_MAKE_CLEAN_FILES ${CMAKE_CURRENT_SOURCE_DIR}/build)
