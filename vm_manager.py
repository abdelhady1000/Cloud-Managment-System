import subprocess, os
from config_manager import get_iso_path

VM_DIR = "vms"

def create_vm_logic(vm_name, cpu, memory, disk):
    os.makedirs(VM_DIR, exist_ok=True)
    disk_path = os.path.join(VM_DIR, f"{vm_name}.qcow2")

    iso = get_iso_path()
    if not iso or not os.path.exists(iso):
        return "Error: ISO not selected or not found"

    if os.path.exists(disk_path):
        return "Error: VM already exists"

    try:
        subprocess.run(["qemu-img","create","-f","qcow2",disk_path,f"{disk}G"],check=True)

        subprocess.Popen([
            "qemu-system-x86_64",
            "-m", str(memory),
            "-smp", str(cpu),
            "-hda", disk_path,
            "-cdrom", iso,
            "-boot", "d"
        ])
        return "Success: VM Creation initiated"
    except Exception as e:
        return f"Error: {str(e)}"
