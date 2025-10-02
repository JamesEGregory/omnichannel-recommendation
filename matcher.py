# matcher.py
import yaml

print(">>> matcher.py loading...")

# --------------------------------------------
# Try importing vendor_loader safely
# --------------------------------------------
try:
    from vendor_loader import load_vendors
    print(">>> vendor_loader import successful")
except Exception as e:
    print(f"!!! vendor_loader import failed: {e}")
    load_vendors = None


# --------------------------------------------
# Main matching function
# --------------------------------------------
def match_vendors(responses):
    """
    Matches council responses to vendor capabilities defined in vendors.yaml.
    Returns a list of (vendor, score) tuples and a justification string.
    """
    if load_vendors is None:
        print("⚠️ load_vendors is None — skipping vendor match")
        return [], "Vendor data could not be loaded."

    # Load vendor data once per run
    vendors = load_vendors()

    # 🔍 Debug prints
    print(">>> RESPONSES:", responses)
    sample_items = list(vendors.items())[:2]
    print(">>> VENDOR DATA SAMPLE:", sample_items)

    scores = []

    for vendor_name, data in vendors.items():
        score = 0

        # Example 1: Automation ambition match
        if responses.get("automation") and "automation_focus" in data:
            if responses["automation"] in data["automation_focus"]:
                score += 3

        # Example 2: Channel strategy match
        if responses.get("omni") and "channel_strategy" in data:
            if responses["omni"] == data["channel_strategy"]:
                score += 2

        # Example 3: Budget band match
        if responses.get("budget") and "budget_band" in data:
            if responses["budget"] == data["budget_band"]:
                score += 1

        if score > 0:
            scores.append((vendor_name, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    if scores:
        top_vendor, top_score = scores[0]
        justification = (
            f"{top_vendor} is recommended because its focus areas align most closely "
            f"with your automation, channel strategy and budget priorities."
        )
    else:
        justification = "No clear vendor match found. Please provide more information or adjust priorities."

    return scores, justification
