# Cloud Management System - Technical Documentation

## Project Overview

The Cloud Management System is a GUI-based application designed to simplify the management of Virtual Machines (VMs) and Docker containers. It provides a unified interface for creating VMs, managing Docker images (searching, building, listing), and controlling Docker containers.

The application leverages standard system tools (`qemu`, `docker`) to perform underlying operations, wrapping them in a user-friendly Python Tkinter interface.

## Technologies Used

*   **Python 3.x**: The core programming language.
*   **Tkinter**: Standard Python interface to the Tcl/Tk GUI toolkit, used for the application interface.
*   **QEMU / KVM**: Open source machine emulator and virtualizer, used for creating and running Virtual Machines.
    *   `qemu-img`: For creating disk images.
    *   `qemu-system-x86_64`: For running the VMs.
*   **Docker Engine**: Used for containerization features.
    *   `docker`: CLI tool used via subprocess calls.
*   **JSON**: Used for storing and retrieving VM configuration data.
*   **Subprocess**: Python module used to execute shell commands for Docker and QEMU operations.

## Project Structure & Function Reference

### 1. Main Application
**File:** `main.py`
The entry point of the application.
*   Initializes the main Tkinter root window.
*   Instantiates the `CloudManagerGUI`.
*   Starts the main event loop.

### 2. GUI Implementation
**File:** `gui.py`
Contains the `CloudManagerGUI` class which defines the user interface and event handlers.

**Key Methods:**
*   `__init__(root)`: Sets up the main window, styles, and notebook tabs.
*   `setup_vm_tab()`: Builds the VM Management tab UI.
*   `setup_docker_image_tab()`: Builds the Docker Image Search tab UI.
*   `setup_container_tab()`: Builds the Live Containers tab UI.
*   `setup_build_tab()`: Builds the Dockerfile Creator and Image Builder tab UI.
*   `create_vm_handler()`: Validates inputs and calls `vm_manager.create_vm_logic`.
*   `load_config_handler()`: Loads VM settings from a JSON file via `config_manager`.
*   `ui_<action>()`: Various wrapper methods (e.g., `ui_search_hub`, `ui_build_image`) that connect GUI buttons to backend logic.

### 3. VM Management
**File:** `vm_manager.py`
Handles logic related to Virtual Machines.

*   `create_vm_logic(vm_name, cpu, memory, disk)`:
    *   Creates a `vms/` directory if it doesn't exist.
    *   Checks for a valid ISO path.
    *   Uses `qemu-img` to create a QCOW2 disk image.
    *   Uses `qemu-system-x86_64` to launch the VM with specified resources (RAM, CPU, Disk, ISO).

### 4. Docker Management
**File:** `docker_manager.py`
Handles interactions with the Docker Engine.

*   `docker_image_list()`: Returns the output of `docker image ls`.
*   `docker_container_list()`: Returns the output of `docker container ls`.
*   `docker_stop_container(container_identifier)`: Stops a container by ID or Name using `docker stop`.
*   `search_local(name)`: Filters local images using `docker images <name>`.
*   `search_hub(name)`: Searches Docker Hub using `docker search <name>`.
*   `save_dockerfile(path, content)`: Writes string content to a `Dockerfile` in the specified directory.
*   `build_image(dockerfile_path, name, tag)`: Executes `docker build` using a dockerfile at the given path.

**File:** `Docker_operations.py`
A CLI helper script for quick Docker operations.
*   `search_local()`: Interactive CLI wrapper for local image search.
*   `search_hub()`: Interactive CLI wrapper for Hub search.
*   `pull_image()`: Interactive CLI wrapper for `docker pull`.

**File:** `image_builder.py`
A CLI helper script for building Docker images.
*   `build_docker_image()`: Interactive function to prompt user for paths and tags, then run `docker build`.

### 5. Configuration
**File:** `config_manager.py`
Manages application configuration and Global state.

*   `set_iso_path(path)`: Updates the global variable holding the selected ISO path.
*   `get_iso_path()`: Retrieves the current ISO path.
*   `load_vm_config(path)`: Parses a JSON file to extract VM parameters (`vm_name`, `cpu`, `memory`, `disk`, `iso_path`). Handles basic validation and error checking.

## Usage Requirements

To run this application, the host system must have:
1.  **Python 3** installed.
2.  **QEMU/KVM** installed and added to the system PATH.
3.  **Docker** installed and running (user must have permissions to run docker commands).
