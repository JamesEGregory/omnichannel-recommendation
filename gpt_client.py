# gpt_client.py
import os, json
from jsonschema import validate, ValidationError
from dotenv import load_dotenv
from openai import OpenAI
from schema import RESPONSE_SCHEMA

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(system_prompt: str, user_prompt: str) -> dict:
    msg = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    resp = client.chat.completions.create(
        model="gpt-5-turbo",  # or "gpt-4o" / your chosen model
        messages=msg,
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    raw = resp.choices[0].message.content
    data = json.loads(raw)
    # Validate against schema
    try:
        validate(instance=data, schema=RESPONSE_SCHEMA)
    except ValidationError as e:
        # Return partial but safe info, with error appended
        data = {"summary": "Schema validation failed; returning raw.", "error": str(e), "raw": raw}
    return data
