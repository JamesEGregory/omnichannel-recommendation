import os
import glob
import yaml

def load_vendor_cards(folder_path: str):
    """Loads all YAML files in the given folder into a dict keyed by vendor name."""
    vendors = {}
    yaml_files = glob.glob(os.path.join(folder_path, "*.yaml"))

    for file_path in yaml_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not data or "name" not in data:
                print(f"⚠️ Skipping {file_path}, missing 'name'")
                continue
            vendors[data["name"]] = data

    return vendors
