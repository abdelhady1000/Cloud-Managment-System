from vm_manager import create_vm
import json

def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("❌ Please enter a valid positive number")

print("Create Virtual Machine")
print("1. Interactive input")
print("2. Configuration file")

choice = input("Choose input method: ")

if choice == "1":
    vm_name = input("VM name: ").strip()
    if not vm_name:
        print("❌ VM name cannot be empty")
        exit()

    cpu = get_positive_int("CPU cores: ")
    memory = get_positive_int("Memory (MB): ")
    disk = get_positive_int("Disk size (GB): ")

elif choice == "2":
    path = input("Config file path: ")

    try:
        with open(path) as f:
            config = json.load(f)

        vm_name = config["vm_name"]
        cpu = int(config["cpu"])
        memory = int(config["memory"])
        disk = int(config["disk"])

    except FileNotFoundError:
        print("❌ Config file not found")
        exit()
    except (KeyError, ValueError):
        print("❌ Invalid config file format")
        exit()

else:
    print("❌ Invalid choice")
    exit()

create_vm(vm_name, cpu, memory, disk)
