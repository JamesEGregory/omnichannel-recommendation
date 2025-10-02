import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (local dev)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------------------
# Primary scoring (simplified example)
# -----------------------------------------
def score_vendors(responses):
    """
    Returns a list of (vendor_name, score) tuples, sorted by score desc.
    Replace this with your full YAML-driven scoring if needed.
    """
    scores = {
        "AWS": 0,
        "Genesys": 0,
        "8x8": 0,
        "RingCentral": 0,
        "Netcall": 0,
        "Cognigy": 0,
        "ICS.ai": 0,
    }

    # Example influence: automation ambition
    automation = responses.get("automation", "")
    if automation == "Switchboard":
        scores["8x8"] += 2
        scores["RingCentral"] += 2
    elif automation == "Complex/agentic":
        scores["Genesys"] += 3
        scores["Cognigy"] += 3
        scores["AWS"] += 2

    # Budget weighting
    budget = responses.get("budget", "")
    if budget == "Low":
        scores["8x8"] += 2
        scores["RingCentral"] += 2
        scores["AWS"] += 1
    elif budget == "High":
        scores["Genesys"] += 2
        scores["Cognigy"] += 2

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    ranked = [(v, s) for v, s in ranked if s > 0]
    return ranked


# -----------------------------------------
# GPT fallback for low maturity / no match
# -----------------------------------------
def get_gpt_fallback_recommendation(responses):
    prompt = f"""
    A UK local council has provided the following answers about their contact centre:
    {responses}

    No clear vendor match was found based on the existing deterministic scoring.
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

    # Try to parse JSON; if fail, return structured fallback
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

    # Take top 1–2 scored vendors
    primary_vendor, primary_score = ranked[0]
    secondary_vendor = ranked[1][0] if len(ranked) > 1 else None

    # Generate natural-language justification with GPT
    justification_prompt = f"""
    The top recommended vendor is {primary_vendor}.
    Secondary option: {secondary_vendor if secondary_vendor else 'None'}.
    Council characteristics: {responses}

    Write a concise explanation (2-3 sentences) for a local authority audience,
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

    # Cost estimation stub (replace with YAML-driven data)
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
    }
