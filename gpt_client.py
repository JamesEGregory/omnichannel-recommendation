# gpt_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env variables (for local development)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_recommendation(responses: dict) -> dict:
    """
    Sends the questionnaire responses to OpenAI and gets back vendor recommendations.
    """
    prompt = f"""
    You are an expert consultant on local government contact centre technology.
    Based on the following council responses, recommend the most suitable vendors
    from the vendor cards provided. Return a structured recommendation with:
    - primary_vendor
    - optional secondary_vendor
    - justification
    - cost_per_agent (if known)
    - total_cost (if num_agents is provided)
    - potential savings (if estimable)

    Responses:
    {responses}
    """

    completion = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for council tech selection."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    text = completion.choices[0].message.content

    # For now, assume GPT returns valid JSON or YAML; you can improve parsing later.
    # Minimal placeholder to avoid breaking:
    return {
        "primary_vendor": "Placeholder Vendor",
        "justification": text,
        "cost_per_agent": "N/A",
        "total_cost": "N/A",
    }
