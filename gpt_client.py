import os
import json
import yaml
from openai import OpenAI
from dotenv import load_dotenv

# -----------------------------------------
# Load environment variables (local dev)
# -----------------------------------------
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------------------
# Load vendor profiles from unified YAML
# -----------------------------------------
with open("vendors.yaml", "r") as f:
    VENDORS = yaml.safe_load(f)


# -----------------------------------------
# Deterministic scoring logic
# -----------------------------------------
def score_vendors(responses):
    """
    Score vendors based on structured YAML attributes and questionnaire responses.
    Returns a sorted list of (vendor_name, score).
    """
    scored = []

    for vendor in VENDORS:
        score = 0

        # 1. Automation ambition alignment
        if responses.get("automation") and responses["automation"] == vendor.get("automation_depth"):
            score += 3

        # 2. Scale fit (very simple match for now)
        agent_size = responses.get("agents")
        if agent_size and str(agent_size) in str(vendor.get("sweet_spot", {}).get("scale", "")):
            score += 2

        # 3. IT capacity alignment
        it_capacity = responses.get("it_capacity")
        if it_capacity and it_capacity in str(vendor.get("sweet_spot", {}).get("it_capacity", "")):
            score += 1

        # 4. Channel strategy / omni capability
        omni = responses.get("omni")
        if omni and vendor.get("channel_support"):
            if omni == "Digital-first" and "Chat" in vendor["channel_support"]:
                score += 1
            elif omni == "True omni-channel orchestration" and len(vendor["channel_support"]) > 3:
                score += 2

        # 5. Budget match (very simplified)
        budget = responses.get("budget")
        if budget == "Low" and vendor.get("pricing_model") and "Consumption" in vendor["pricing_model"]:
            score += 2
        elif budget == "High" and vendor.get("pricing_model") and "Subscription" in vendor["pricing_model"]:
            score += 1

        if score > 0:
            scored.append((vendor["name"], score))

    return sorted(scored, key=lambda x: x[1], reverse=True)


# -----------------------------------------
# GPT fallback logic for low maturity / no match
# -----------------------------------------
def get_gpt_fallback_recommendation(responses):
    prompt = f"""
    A UK local authority has provided the following answers about their contact centre:
    {json.dumps(responses, indent=2)}

    No deterministic vendor scored well.

    Recommend one or two *starter* omni-channel contact centre platforms that are:
    - Suitable for councils with low maturity
    - Cost effective
    - Easy to integrate with basic telephony
    - Scalable for future channel expansion

    Return a JSON object with:
    - primary_vendor
    - secondary_vendor (optional)
    - justification
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
# Natural language justification for scored vendors
# -----------------------------------------
def generate_justification(primary_vendor, secondary_vendor, responses):
    prompt = f"""
    The top recommended vendor is {primary_vendor}.
    Secondary option: {secondary_vendor if secondary_vendor else 'None'}.

    Council characteristics:
    {json.dumps(responses, indent=2)}

    Write a concise 2–3 sentence explanation, suitable for a UK local authority audience,
    justifying why this vendor is a good fit based on their priorities, size, and maturity.
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "You are an expert in UK local government contact centre technology."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.output_text.strip()


# -----------------------------------------
# Main orchestration
# -----------------------------------------
def get_recommendation(responses):
    ranked = score_vendors(responses)

    # ✅ If no vendors matched, use GPT fallback
    if not ranked:
        return get_gpt_fallback_recommendation(responses)

    # Top vendor(s)
    primary_vendor, primary_score = ranked[0]
    secondary_vendor = ranked[1][0] if len(ranked) > 1 else None

    justification = generate_justification(primary_vendor, secondary_vendor, responses)

    # Simplified cost estimation (placeholder)
    cost_per_agent = 75
    total_cost = 75 * 100
    savings = 10000

    return {
        "primary_vendor": primary_vendor,
        "secondary_vendor": secondary_vendor,
        "justification": justification,
        "cost_per_agent": cost_per_agent,
        "total_cost": total_cost,
        "savings": savings
    }
