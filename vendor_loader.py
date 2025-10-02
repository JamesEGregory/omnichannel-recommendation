# vendor_loader.py
import yaml
import os

def load_vendor_cards(file_path="vendors.yaml"):
    """
    Loads all vendor information from a single vendors.yaml file.
    Returns a dictionary keyed by vendor name.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Vendor file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("vendors.yaml must contain a top-level dictionary")

    return data
