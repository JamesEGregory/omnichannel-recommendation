from vendor_loader import load_vendor_cards

if __name__ == "__main__":
    vendors = load_vendor_cards()
    print(f"✅ Loaded {len(vendors)} vendor cards")
    for v in vendors:
        print(f"- {v['name']}")
