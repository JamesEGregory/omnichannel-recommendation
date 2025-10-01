# schema.py
RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["summary", "recommendations", "assumptions", "gaps", "confidence"],
    "properties": {
        "summary": {"type": "string"},
        "confidence": {"type": "object",
            "required": ["score", "label"],
            "properties": {
                "score": {"type": "number", "minimum": 0, "maximum": 100},
                "label": {"type": "string"}
            }},
        "recommendations": {"type": "array", "minItems": 1,
            "items": {
                "type": "object",
                "required": ["vendor", "fit_percent", "fit_label", "why", "watchouts",
                             "est_price_band", "deployment_time", "key_integrations"],
                "properties": {
                    "vendor": {"type": "string"},
                    "fit_percent": {"type": "number"},
                    "fit_label": {"type": "string"},
                    "why": {"type": "string"},
                    "watchouts": {"type": "string"},
                    "est_price_band": {"type": "string"},
                    "deployment_time": {"type": "string"},
                    "key_integrations": {"type": "array", "items": {"type": "string"}}
                }
            }},
        "assumptions": {"type": "array", "items": {"type": "string"}},
        "gaps": {"type": "array", "items": {"type": "string"}},
        "comparison_table": {"type": "array",
            "items": {
                "type": "object",
                "required": ["vendor", "fit", "channels", "telephony_teams", "crm", "back_office", "automation_depth", "wem_analytics"],
                "properties": {
                    "vendor": {"type": "string"},
                    "fit": {"type": "string"},
                    "channels": {"type": "string"},
                    "telephony_teams": {"type": "string"},
                    "crm": {"type": "string"},
                    "back_office": {"type": "string"},
                    "automation_depth": {"type": "string"},
                    "wem_analytics": {"type": "string"}
                }
            }}
    }
}
