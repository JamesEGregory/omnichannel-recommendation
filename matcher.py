# matcher.py
from vendor_loader import load_vendor_cards

# --------------------------------------------
# 1. Define weightings for each questionnaire field
# --------------------------------------------
WEIGHTS = {
    "agents": 2,
    "it_capacity": 2,
    "channels_now": 2,
    "telephony": 3,
    "crm": 3,
    "pain_points": 2,
    "priorities": 3,
    "budget": 3,
    "timescale": 2,
    "expected_spend": 3
}

# --------------------------------------------
# 2. Helper functions
# --------------------------------------------
def match_scale(vendor, agents_answer):
    """Check if vendor's sweet spot matches number of agents."""
    scale_text = vendor["sweet_spot"]["scale"].lower()
    return any(keyword in scale_text for keyword in agents_answer.lower().split())

def match_it_capacity(vendor, it_capacity_answer):
    """Check if vendor matches IT capacity level."""
    return it_capacity_answer.lower() in vendor["sweet_spot"]["it_capacity"].lower()

def match_channels(vendor, selected_channels):
    """Check if vendor supports the required channels."""
    vendor_channels = vendor.get("channels", {})
    score = 0
    for ch in selected_channels:
        if ch.lower() == "voice" and vendor_channels.get("voice"):
            score += 1
        elif ch.lower() == "webchat" and vendor_channels.get("chat"):
            score += 1
        elif ch.lower() == "email" and vendor_channels.get("email"):
            score += 1
        elif ch.lower() in [s.lower() for s in vendor_channels.get("social", [])]:
            score += 1
    return score / max(1, len(selected_channels))  # normalize 0–1

def match_telephony(vendor, telephony_answer):
    """Check PBX/Teams compatibility."""
    telephony_info = vendor.get("integrations", {}).get("telephony", {}).get("pbx_teams", "").lower()
    return telephony_answer.lower() in telephony_info

def match_crm(vendor, crm_answer):
    """Check CRM compatibility."""
    supported_crms = [c.lower() for c in vendor.get("integrations", {}).get("crm", {}).get("supported", [])]
    return crm_answer.lower() in supported_crms

def match_budget(vendor, budget_answer):
    """Roughly match based on pricing_band."""
    band = vendor.get("commercials", {}).get("pricing_band", "").lower()
    return budget_answer.lower() in band

# --------------------------------------------
# 3. Main function to rank vendors
# --------------------------------------------
def rank_vendors(responses):
    vendors = load_vendor_cards()
    scores = []

    for vendor in vendors:
        vendor_name = vendor.get("name", "Unknown")
        score = 0
        max_score = 0

        # Agents / scale
        if "agents" in responses:
            max_score += WEIGHTS["agents"]
            if match_scale(vendor, responses["agents"]):
                score += WEIGHTS["agents"]

        # IT capacity
        if "it_capacity" in responses:
            max_score += WEIGHTS["it_capacity"]
            if match_it_capacity(vendor, responses["it_capacity"]):
                score += WEIGHTS["it_capacity"]

        # Channels
        if "channels_now" in responses:
            max_score += WEIGHTS["channels_now"]
            score += WEIGHTS["channels_now"] * match_channels(vendor, responses["channels_now"])

        # Telephony
        if "telephony" in responses:
            max_score += WEIGHTS["telephony"]
            if match_telephony(vendor, responses["telephony"]):
                score += WEIGHTS["telephony"]

        # CRM
        if "crm" in responses:
            max_score += WEIGHTS["crm"]
            if match_crm(vendor, responses["crm"]):
                score += WEIGHTS["crm"]

        # Budget
        if "budget" in responses:
            max_score += WEIGHTS["budget"]
            if match_budget(vendor, responses["budget"]):
                score += WEIGHTS["budget"]

        # Add future matching logic for pain_points, priorities, expected_spend, etc

        # Final normalized score (0–100)
        if max_score > 0:
            final_score = (score / max_score) * 100
        else:
            final_score = 0

        scores.append((vendor_name, round(final_score, 1)))

    # Sort vendors by score
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores
