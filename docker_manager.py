import subprocess, os

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
    
def search_local(name):
    result = subprocess.run(['docker', 'images', name], capture_output=True, text=True)
    return result.stdout

def search_hub(name):
    result = subprocess.run(['docker', 'search', name], capture_output=True, text=True)
    return result.stdout

def save_dockerfile(path, content):
    try:
        os.makedirs(path, exist_ok=True)
        dockerfile_path = os.path.join(path, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write(content)
        return f"Dockerfile saved at: {dockerfile_path}"
    except Exception as e:
        return f"Error: {str(e)}"

def build_image(dockerfile_path, name, tag):
    if not os.path.exists(dockerfile_path):
        return "Error: Dockerfile not found!"
    
    build_context = os.path.dirname(dockerfile_path)
    command = ["docker", "build", "-t", f"{name.lower()}:{tag}", build_context]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout + "\nDocker image build finished"
    except Exception as e:
        return f"Error: {str(e)}"
