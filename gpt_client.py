import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (mainly for local dev — Railway will use env vars)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------------------
# Primary scoring (placeholder or your own scoring function)
# -----------------------------------------
def score_vendors(responses):
    """
    Returns a list of (vendor_name, score) tuples, sorted by score desc.
    This should be replaced with your actual vendor scoring logic.
    """
    # Example: super simple scoring stub
    scores = {
        "AWS": 0,
        "Genesys": 0,
        "8x8": 0,
        "RingCentral": 0,
        "Netcall": 0,
        "Cognigy": 0,
        "ICS.ai": 0,
    }

    # Sample influence: automation ambition
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

    # Return sorted vendor list
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    # Filter out zero scores
    ranked = [(v, s) for v, s in ranked if s > 0]
    return ranked


# -----------------------------------------
# GPT fallback prompt for low-maturity / no clear match
# -----------------------------------------
def get_gpt_fallback_recommendation(responses):
    """
    Uses GPT to suggest starter vendors when deterministic scoring yields no match.
    """
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
        reasoning={"effort": "medium"},
        input=[
            {"role": "system", "content": "You are an expert in UK local government contact centre technology."},
            {"role": "user", "content": prompt}
        ]
    )

    # Try to parse the structured JSON
    try:
        content = response.output_text.strip()
        import json
        return json.loads(content)
    except Exception:
        # If GPT returns something slightly off, just return the raw text
        return {"primary_vendor": None, "justification": content}


# -----------------------------------------
# Main orchestration
# -----------------------------------------
def get_recommendation(responses):
    ranked = score_vendors(responses)

    if not ranked:
        # Fallback path: no scored vendors
        return get_gpt_fallback_recommendation(responses)

    # If we have scored vendors, take top 1–2 and return formatted response
    primary_vendor, primary_score = ranked[0]
    secondary_vendor = ranked[1][0] if len(ranked) > 1 else None

    # Justification can also be GPT-generated if you want richer text
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

    # Cost estimation stub (you can replace this with real logic)
    cost_per_agent = 75
    total_cost = 75 * 100  # assuming 100 agents as placeholder
    savings = 10000  # stub

    return {
        "primary_vendor": primary_vendor,
        "secondary_vendor": secondary_vendor,
        "justification": justification,
        "cost_per_agent": cost_per_agent,
        "total_cost": total_cost,
        "savings": savings
    }
