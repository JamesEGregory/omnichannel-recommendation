import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_recommendation(responses, vendors):
    """
    Sends questionnaire responses + vendor data to GPT to get structured recommendations.
    """
    vendor_descriptions = "\n\n".join(
        [f"{v['name']}: {v.get('summary', '')}" for v in vendors.values()]
    )

    user_input = "\n".join([f"{k}: {v}" for k, v in responses.items()])

    prompt = f"""
    You are an expert advisor on UK local government contact centre technology.
    Based on the following council context:

    {user_input}

    And these vendor capabilities:

    {vendor_descriptions}

    Recommend the best-fit vendor. Return JSON with:
    - primary_vendor
    - secondary_vendor (optional)
    - justification (short)
    - cost_per_agent (if applicable)
    - total_cost (if applicable)
    - savings (if applicable)
    """

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt,
        temperature=0.3
    )

    content = response.output_text
    import json
    return json.loads(content)
