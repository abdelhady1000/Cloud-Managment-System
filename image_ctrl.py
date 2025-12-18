import subprocess
def docker_image_list():
    result = subprocess.run(["docker","image","ls"], capture_output=True, text=True)
    return result.stdout
def docker_container_list():
    result = subprocess.run(["docker","container","ls"], capture_output=True, text=True)
    return result.stdout
def docker_stop_container(container_identifier : str):
    result = subprocess.run(["docker","stop", container_identifier], capture_output=True, text=True)
    if result.returncode == 0:
        return f"Successfully stopped container {container_identifier}"
    else:
        return "Invalid container ID/Name, please retry again."