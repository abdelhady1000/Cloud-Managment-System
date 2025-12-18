import subprocess
import os

ISO_PATH = "iso/ubuntu-20.04.6-desktop-amd64.iso"
VM_DIR = "vms"

def create_vm(vm_name, cpu, memory, disk):
    os.makedirs(VM_DIR, exist_ok=True)
    disk_path = os.path.join(VM_DIR, f"{vm_name}.qcow2")

    if not os.path.exists(ISO_PATH):
        print("❌ Ubuntu ISO not found")
        return

    if os.path.exists(disk_path):
        print("❌ VM already exists")
        return

    try:
        subprocess.run([
            "qemu-img", "create", "-f", "qcow2",
            disk_path, f"{disk}G"
        ], check=True)

        print("✅ Virtual disk created")

        subprocess.run([
            "qemu-system-x86_64",
            "-m", str(memory),
            "-smp", str(cpu),
            "-hda", disk_path,
            "-cdrom", ISO_PATH,
            "-boot", "d"
        ])

    except subprocess.CalledProcessError:
        print("❌ Failed to create or start VM")
