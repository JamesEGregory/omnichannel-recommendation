from gpt_client import get_recommendation

# Define a few example personas to test vendor spread
personas = [
    {"agents": "<20", "automation": "Switchboard", "omni": "Voice-first + digital"},
    {"agents": "100–300", "automation": "Complex/agentic", "omni": "True omni-channel orchestration"},
    {"agents": "20–100", "automation": "Service requests", "omni": "Digital-first"},
]

for i, p in enumerate(personas, start=1):
    print(f"\n--- Persona {i} ---")
    try:
        rec = get_recommendation(p)
        print(f"Primary: {rec.get('primary_vendor')}")
        print(f"Secondary: {rec.get('secondary_vendor')}")
        print(f"Rationale: {rec.get('justification')}")
    except Exception as e:
        print(f"Error for persona {i}: {e}")
