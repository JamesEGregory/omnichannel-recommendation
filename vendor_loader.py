# vendor_loader.py
import os
import yaml

def load_vendors(vendors_folder: str = "vendors"):
    """
    Load all vendor YAML files from the given folder and return a dictionary
    keyed by vendor name (taken from the 'name' field inside each YAML file).
    """
    vendors = {}

    if not os.path.exists(vendors_folder):
        raise FileNotFoundError(f"Vendors folder '{vendors_folder}' not found")

    for filename in os.listdir(vendors_folder):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            filepath = os.path.join(vendors_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f)
                    if data and "name" in data:
                        vendors[data["name"]] = data
                    else:
                        print(f"⚠️ {filename} has no 'name' field — skipped")
                except yaml.YAMLError as e:
                    print(f"⚠️ Failed to parse {filename}: {e}")

    if not vendors:
        raise ValueError(f"No valid vendor files found in '{vendors_folder}'")

    return vendors
