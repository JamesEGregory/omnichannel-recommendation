# test_personas.py

from gpt_client import get_recommendation

PERSONAS = {
    "A - Small voice-first, low automation": {
        "strategy": ["Cost savings"],
        "automation": "Switchboard",
        "omni": "Voice-first + digital",
        "hand_off": "No",
        "integration": "Manual/siloed",
        "back_office": "None",
        "procurement": "Subscription (per agent/month)",
        "delivery": "Turnkey vendor",
        "lock_in": "Not a concern",
        "ms_bias": "No",
        "demand_profile": "<20 agents / low volume",
        "budget": "Low"
    },
    "B - Mid-size, improving service, moderate IT": {
        "strategy": ["CX improvement", "Channel shift"],
        "automation": "Service requests",
        "omni": "Voice-first + digital",
        "hand_off": "Yes",
        "integration": "Point-to-point",
        "back_office": "CRM + Housing",
        "procurement": "Subscription (per agent/month)",
        "delivery": "Hybrid (partner + in-house)",
        "lock_in": "Important",
        "ms_bias": "Mixed/Unsure",
        "demand_profile": "20–100 agents",
        "budget": "Medium"
    },
    "C - Large, digital-first, complex": {
        "strategy": ["Automation/AI", "CX improvement", "Data/insight"],
        "automation": "Complex/agentic",
        "omni": "True omni-channel orchestration",
        "hand_off": "Yes",
        "integration": "Mature integration platform",
        "back_office": "CRM, ERP, Social care",
        "procurement": "Subscription (per agent/month)",
        "delivery": "Open platform we control",
        "lock_in": "Critical",
        "ms_bias": "No",
        "demand_profile": "300+ agents",
        "budget": "High"
    },
    "D - Lock-in averse, integration focused": {
        "strategy": ["Integration/workflow", "Automation/AI"],
        "automation": "Transactions",
        "omni": "Digital-first",
        "hand_off": "Yes",
        "integration": "Middleware/APIs",
        "back_office": "Various",
        "procurement": "Consumption (pay per use)",
        "delivery": "Hybrid (partner + in-house)",
        "lock_in": "Critical",
        "ms_bias": "No",
        "demand_profile": "100–300 agents",
        "budget": "Medium"
    },
    "E - Public sector workflow focus": {
        "strategy": ["Channel shift", "CX improvement"],
        "automation": "Service requests",
        "omni": "Voice-first + digital",
        "hand_off": "Yes",
        "integration": "Point-to-point",
        "back_office": "CRM, Revenues & Benefits",
        "procurement": "Subscription (per agent/month)",
        "delivery": "Turnkey vendor",
        "lock_in": "Important",
        "ms_bias": "Yes",
        "demand_profile": "20–100 agents",
        "budget": "Medium"
    }
}

if __name__ == "__main__":
    print("🧪 Running vendor recommendation tests for personas...\n")
    for name, answers in PERSONAS.items():
        print(f"--- {name} ---")
        try:
            rec = get_recommendation(answers)
            print(f"Primary vendor: {rec.get('primary_vendor')}")
            if rec.get("secondary_vendor"):
                print(f"Secondary vendor: {rec['secondary_vendor']}")
            print(f"Justification: {rec.get('justification', 'N/A')}")
        except Exception as e:
            print(f"❌ Error generating recommendation for {name}: {e}")
        print("\n")
