import os

def create_dockerfile():
    print("\nDockerfile Creator")
    print("Write Dockerfile lines one by one")
    print("Type DONE when finished\n")

    path = input("Folder to save Dockerfile: ")
    os.makedirs(path, exist_ok=True)

    dockerfile_path = os.path.join(path, "Dockerfile")

    lines = []
    while True:
        line = input("> ")
        if line.upper() == "DONE":
            break
        lines.append(line)

    with open(dockerfile_path, "w") as f:
        for l in lines:
            f.write(l + "\n")

    print("Dockerfile saved at:", dockerfile_path)

if __name__ == "__main__":
    create_dockerfile()
