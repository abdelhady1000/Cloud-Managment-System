import os
import subprocess

def build_docker_image():
    print("\nDocker Image Builder")

    dockerfile_path = input("Enter path to Dockerfile: ").strip()

    if not os.path.exists(dockerfile_path):
        print("Dockerfile not found!")
        return

    image_name = input("Enter image name: ").lower().strip()
    image_tag = input("Enter image tag: ").strip()

    build_context = os.path.dirname(dockerfile_path)

    command = [
        "docker", "build",
        "-t", f"{image_name}:{image_tag}",
        build_context
    ]

    subprocess.run(command)

    print("Docker image build finished")

if __name__ == "__main__":
    build_docker_image()
