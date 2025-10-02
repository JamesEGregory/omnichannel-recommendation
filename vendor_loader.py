# vendor_loader.py
import os
import yaml

def load_vendor_cards(vendors_folder: str = "vendors"):
    """
    Load all vendor YAML files from the given folder and return as a list of dicts.
    Each file must contain valid YAML following the agreed vendor structure.
    """
    vendors = []

    if not os.path.exists(vendors_folder):
        raise FileNotFoundError(f"Vendors folder '{vendors_folder}' not found")

    for filename in os.listdir(vendors_folder):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            filepath = os.path.join(vendors_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f)
                    if data:  # ignore empty files
                        vendors.append(data)
                except yaml.YAMLError as e:
                    print(f"⚠️ Failed to parse {filename}: {e}")

    if not vendors:
        raise ValueError(f"No valid vendor files found in '{vendors_folder}'")

    return vendors
