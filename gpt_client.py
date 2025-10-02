import os
import json
import yaml
from dotenv import load_dotenv
from openai import OpenAI
from glob import glob

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ------------------------------
# Load all vendor YAML cards
# ------------------------------
def load_vendor_cards():
    vendor_files = glob("*.yaml") + glob("vendors/*.yaml")
    vendors = {}
    for vf in vendor_files:
        with open(vf, "r") as f:
            data = yaml.safe_load(f)
            if data and "name" in data:
                vendors[data["name"]] = data
    return vendors


VENDOR_CARDS = load_vendor_cards()


# ------------------------------
# Scoring logic
# ------------------------------
def score_vendors(responses):
    """
    Score vendors based on simple keyword / option matching against their sweet spots,
    strengths, integrations, etc. This is lightweight but uses the YAML metadata.
    """
    scores = {name: 0 for name in VENDOR_CARDS.keys()}

    for vendor_name, card in VENDOR_CARDS.items():
        # Example: scale / sweet spot
        scale = responses.get("agents")
        if scale and "sweet_spot" in card:
            if scale in str(card["sweet_spot"]):
                scores[vendor_name] += 2

        # Example: automation ambition vs automation depth
        automation = responses.get("automation")
        if automation and "automation_depth" in card:
            if automation.lower() in str(card["automation_depth"]).lower():
                scores[vendor_name] += 3

        # Example: channel strategy vs coverage
        omni = responses.get("omni")
        if omni and "channel_coverage" in card:
            if omni.lower().split()[0] in str(card["channel_coverage"]).lower():
                scores[vendor_name] += 2

        # Example: CRM / Telephony integration
        crm = responses.get("crm")
        if crm and "integrations" in card:
            crm_section = card["integrations"].get("crm", [])
            if crm in crm_section:
                scores[vendor_name] += 2

        telephony = responses.get("telephony")
        if telephony and "integrations" in card:
            tele_section = card["integrations"].get("telephony", [])
            if telephony in tele_section:
                scores[vendor_name] += 2

        # Budget influence
        budget = responses.get("budget")
        if budget and "commercials" in card:
            price_band = str(card["commercials"].get("price_band", "")).lower()
            if budget.lower() in price_band:
                scores[vendor_name] += 1

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    ranked = [(v, s) for v, s in ranked if s > 0]
    return ranked


# ------------------------------
# GPT Fallback for low maturity
# ------------------------------
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

    Return the response in the following JSON structure:

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


# ------------------------------
# Main orchestration
# ------------------------------
def get_recommendation(responses):
    ranked = score_vendors(responses)

    # If no match, use GPT fallback
    if not ranked:
        return get_gpt_fallback_recommendation(responses)

    primary_vendor, primary_score = ranked[0]
    secondary_vendor = ranked[1][0] if len(ranked) > 1 else None

    # Justification via GPT
    justification_prompt = f"""
    The top recommended vendor is {primary_vendor}.
    Secondary option: {secondary_vendor if secondary_vendor else 'None'}.
    Council characteristics: {responses}

    Write a concise explanation (2–3 sentences) for a local authority audience,
    justifying why this vendor is a good fit based on their priorities and constraints.
    """

    justification_response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "You are an expert in UK local government contact centre technology."},
            {"role": "user", "content": justification_prompt}
        ]
    )

    justification = justification_response.output_text.strip()

    # Basic cost estimate — replace with real data from YAML later
    cost_per_agent = 75
    total_cost = 75 * 100  # placeholder for 100 agents
    savings = 10000  # placeholder

    return {
        "primary_vendor": primary_vendor,
        "secondary_vendor": secondary_vendor,
        "justification": justification,
        "cost_per_agent": cost_per_agent,
        "total_cost": total_cost,
        "savings": savings
