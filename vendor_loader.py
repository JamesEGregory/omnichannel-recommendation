import os
import glob
import yaml

def load_vendor_cards(vendor_folder="."):
    """
    Loads all vendor YAML files from the given folder into a dictionary.
    Each YAML file should define a single vendor profile.
    """
    vendor_cards = {}
    yaml_files = glob.glob(os.path.join(vendor_folder, "*.yaml"))

    for file_path in yaml_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data and "name" in data:
                vendor_name = data["name"]
                vendor_cards[vendor_name] = data

    return vendor_cards

if __name__ == "__main__":
    # Quick check
    cards = load_vendor_cards(".")
    print(f"Loaded {len(cards)} vendor profiles: {list(cards.keys())}")
