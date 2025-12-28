import json, os

ISO_PATH = None

def set_iso_path(path):
    global ISO_PATH
    ISO_PATH = path

def get_iso_path():
    return ISO_PATH

def load_vm_config(path):
    try:
        with open(path) as f:
            config = json.load(f)

        vm_name = config["vm_name"]
        cpu = int(config["cpu"])
        memory = int(config["memory"])
        disk = int(config["disk"])

        if "iso_path" in config and os.path.exists(config["iso_path"]):
            set_iso_path(config["iso_path"])

        return vm_name, cpu, memory, disk

    except FileNotFoundError:
        return None, "Config file not found"
    except (KeyError, ValueError, json.JSONDecodeError):
        return None, "Invalid config file format"
