import subprocess

def search_local():
    name = input("Enter the image name/tag to search locally: ")
    print(f"\nSearching locally for '{name}'...")
    subprocess.run(['docker', 'images', name])

def search_hub():
    name = input("Enter the image name to search on DockerHub: ")
    print(f"\nSearching DockerHub for '{name}'...")
    subprocess.run(['docker', 'search', name])

def pull_image():
    name = input("Enter the image name to pull from DockerHub: ")
    print(f"\nPulling image '{name}'...")
    subprocess.run(['docker', 'pull', name])

if __name__ == "__main__":
    while True:
        print("\n=== Cloud Management System ===")
        print("1. Search Local Image")
        print("2. Search DockerHub")
        print("3. Download/Pull Image")
        print("4. Exit")
        
        choice = input("Select an option: ")
        if choice == '1': search_local()
        elif choice == '2': search_hub()
        elif choice == '3': pull_image()
        elif choice == '4': break
        else: print("Invalid choice.")