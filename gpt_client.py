# gpt_client.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from vendor_loader import load_vendor_cards

# -----------------------------------------
# Environment setup
# -----------------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load all vendor data from vendors.yaml
VENDORS = load_vendor_cards()

# -----------------------------------------
# Vendor scoring function (data-driven)
# -----------------------------------------
def score_vendors(responses):
    """
    Scores vendors based on simple matching rules
    using fields from the questionnaire and vendor YAML data.
    This can be made as sophisticated as you like.
    """
    scores = {vendor: 0 for vendor in VENDORS.keys()}

    # Automation ambition match (example)
    automation = responses.get("automation", "")
    for vendor, data in VENDORS.items():
        sweet_spot = data.get("sweet_spot", {})
        if automation and "automation" in sweet_spot:
            if automation in sweet_spot["automation"]:
                scores[vendor] += 3

    # Budget match (if present)
    budget = responses.get("budget", "")
    for vendor, data in VENDORS.items():
        commercials = data.get("commercials", {})
        if budget and "typical_band" in commercials:
            if budget.lower() in [b.lower() for b in commercials["typical_band"]]:
                scores[vendor] += 2

    # Channel / integration alignment
    channels = responses.get("channels_now", [])
    if isinstance(channels, str):
        channels = [channels]

    for vendor, data in VENDORS.items():
        vendor_channels = data.get("channels", [])
        for ch in channels:
            if ch in vendor_channels:
                scores[vendor] += 1

    # IT capacity / delivery model
    it_capacity = responses.get("it_capacity", "")
    for vendor, data in VENDORS.items():
        if "it_capacity_fit" in data and it_capacity in data["it_capacity_fit"]:
            scores[vendor] += 2

    # Integration maturity (example)
    integration_level = responses.get("integration", "")
    for vendor, data in VENDORS.items():
        if "integration_fit" in data and integration_level in data["integration_fit"]:
            scores[vendor] += 2

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    ranked = [(v, s) for v, s in ranked if s > 0]
    return ranked

# -----------------------------------------
# GPT fallback if no deterministic match
# -----------------------------------------
def get_gpt_fallback_recommendation(responses):
    prompt = f"""
    A UK local council has provided the following answers about their contact centre:
    {responses}

    No clear vendor match was found based on the deterministic scoring.
    Recommend one or two *starter* omni-channel contact centre platforms that are:
    - Suitable for councils with low maturity
    - Cost effective
    - Easy to integrate with basic telephony
    - Scalable for future channel expansion

    Return the response in this JSON structure:
    {{
        "primary_vendor": "...",
        "secondary_vendor": "...",
        "justification": "..."
    }}
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "You are an expert in UK local government contact centre technology."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.output_text.strip()
    try:
        return json.loads(content)
    except Exception:
        return {
            "primary_vendor": None,
            "secondary_vendor": None,
            "justification": content
        }

# -----------------------------------------
# Main orchestration
# -----------------------------------------
def get_recommendation(responses):
    ranked = score_vendors(responses)

    if not ranked:
        # Fallback path: no scored vendors
        return get_gpt_fallback_recommendation(responses)

    primary_vendor, primary_score = ranked[0]
    secondary_vendor = ranked[1][0] if len(ranked) > 1 else None

    # Generate justification with GPT
    justification_prompt = f"""
    The top recommended vendor is {primary_vendor}.
    Secondary option: {secondary_vendor if secondary_vendor else 'None'}.
    Council characteristics: {responses}

    Write a concise explanation (2–3 sentences) for a local authority audience,
    justifying why this vendor is a good fit based on their priorities.
    """

    justification_response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "You are an expert in UK local government contact centre technology."},
            {"role": "user", "content": justification_prompt}
        ]
    )

    justification = justification_response.output_text.strip()

    # Placeholder cost estimation — can later use YAML values
    cost_per_agent = 75
    total_cost = 75 * 100  # placeholder for 100 agents
    savings = 10000       # placeholder

    return {
        "primary_vendor": primary_vendor,
        "secondary_vendor": secondary_vendor,
        "justification": justification,
        "cost_per_agent": cost_per_agent,
        "total_cost": total_cost,
        "savings": savings
    }
