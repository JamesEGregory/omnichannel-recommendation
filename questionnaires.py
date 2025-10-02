# questionnaires.py

# --------------------------------------------------
# Discovery Questionnaire
# (For councils early in their thinking)
# --------------------------------------------------
DISCOVERY = [
    {
        "id": "agents",
        "label": "Approx. number of agents",
        "type": "select",
        "options": ["<20", "20–100", "100–300", "300+"]
    },
    {
        "id": "structure",
        "label": "How are teams structured?",
        "type": "select",
        "options": ["Single central centre", "Multiple departmental teams", "Mixed", "Not sure"]
    },
    {
        "id": "channels_now",
        "label": "Channels in use (select all)",
        "type": "multiselect",
        "options": ["Voice", "Webchat", "Email", "SMS", "Social", "Self-service portal", "In-person"]
    },
    {
        "id": "channel_pain",
        "label": "Which channel causes most pain?",
        "type": "select",
        "options": ["Voice", "Email", "Webchat", "Social", "Not sure"]
    },
    {
        "id": "top_services",
        "label": "Top interaction drivers (free text)",
        "type": "text"
    },
    {
        "id": "telephony",
        "label": "Telephony estate",
        "type": "select",
        "options": ["Avaya", "Cisco", "Mitel", "Teams Voice", "8x8", "RingCentral", "Other/Unknown"]
    },
    {
        "id": "crm",
        "label": "CRM / case management",
        "type": "select",
        "options": ["Dynamics 365", "Salesforce", "Netcall Liberty", "Civica", "Capita ONE", "ServiceNow", "None/Unknown"]
    },
    {
        "id": "self_service",
        "label": "Self-service / portal adoption",
        "type": "select",
        "options": ["None/basic", "Some services", "Widely used", "Not sure"]
    },
    {
        "id": "pain_points",
        "label": "Biggest operational pain (select up to 3)",
        "type": "multiselect",
        "options": [
            "Long queues",
            "Multi-channel demand mgmt",
            "Poor integration",
            "Limited automation",
            "Inconsistent CX",
            "Aging PBX",
            "Weak MI/analytics"
        ]
    },
    {
        "id": "priorities",
        "label": "Top 2–3 priorities",
        "type": "multiselect",
        "options": [
            "Cost savings",
            "Improve CX",
            "Channel expansion",
            "Upgrade telephony",
            "Integration/workflow",
            "Resilience/BCP"
        ]
    },
    {
        "id": "it_capacity",
        "label": "Internal IT/dev capacity",
        "type": "select",
        "options": ["Low", "Medium", "High", "Not sure"]
    },
    {
        "id": "budget",
        "label": "Budget band (run + change)",
        "type": "select",
        "options": ["Low", "Medium", "High", "Unknown"]
    },
    {
        "id": "urgency",
        "label": "Target go-live timescale",
        "type": "select",
        "options": ["<3 months", "3–6 months", "6–12 months", "12+ months"]
    },
    {
        "id": "security",
        "label": "Security/sovereignty driver",
        "type": "select",
        "options": ["Yes", "No", "Not sure"]
    },
    {
        "id": "uk_support",
        "label": "Require UK-based support?",
        "type": "select",
        "options": ["Yes", "No", "Not sure"]
    }
]

# --------------------------------------------------
# Diagnostic Questionnaire
# (For councils with a clearer strategy)
# --------------------------------------------------
DIAGNOSTIC = [
    {
        "id": "channel_strategy",
        "label": "Do you have a defined channel strategy?",
        "type": "select",
        "options": ["Yes", "In progress", "No"]
    },
    {
        "id": "automation_roadmap",
        "label": "Have you defined an automation roadmap?",
        "type": "select",
        "options": ["Yes", "In progress", "No"]
    },
    {
        "id": "automation_scope",
        "label": "How far do you intend to go with automation?",
        "type": "select",
        "options": [
            "Switchboard / FAQ only",
            "Service requests",
            "Transactional",
            "Complex workflows / end-to-end resolution"
        ]
    },
    {
        "id": "integration_complexity",
        "label": "How complex are your integrations?",
        "type": "select",
        "options": ["Low", "Medium", "High"]
    },
    {
        "id": "preferred_telephony",
        "label": "What is your current / target telephony platform?",
        "type": "select",
        "options": ["Avaya", "Cisco", "Mitel", "Teams Voice", "8x8", "RingCentral", "Cloud PBX", "Other"]
    },
    {
        "id": "crm_system",
        "label": "What CRM or case management system do you use?",
        "type": "select",
        "options": ["Dynamics 365", "Salesforce", "Netcall Liberty", "Civica", "Capita ONE", "ServiceNow", "Other", "None"]
    },
    {
        "id": "back_office",
        "label": "Which key back-office systems do you need to integrate with?",
        "type": "multiselect",
        "options": [
            "Revenues & Benefits",
            "Waste",
            "Planning / Building Control",
            "Housing",
            "Adult Social Care",
            "Children’s Social Care",
            "Environmental Health / Licensing",
            "Custom / Other"
        ]
    },
    {
        "id": "channel_priorities",
        "label": "Which channels are your top priorities to improve?",
        "type": "multiselect",
        "options": ["Voice", "Chat", "Email", "Social", "Self-service", "All equally"]
    },
    {
        "id": "cx_vs_cost",
        "label": "What’s the main strategic driver?",
        "type": "select",
        "options": [
            "Primarily cost savings",
            "Balanced cost & CX",
            "Primarily customer experience"
        ]
    },
    {
        "id": "timescale",
        "label": "Target timescale for implementation",
        "type": "select",
        "options": ["<3 months", "3–6 months", "6–12 months", "12+ months"]
    },
    {
        "id": "it_capacity",
        "label": "Internal IT/developer capacity",
        "type": "select",
        "options": ["Low", "Medium", "High", "Not sure"]
    },
    {
        "id": "budget",
        "label": "Indicative budget",
        "type": "select",
        "options": ["Low", "Medium", "High", "Unknown"]
    },
    {
        "id": "security",
        "label": "Is security / data sovereignty a key factor?",
        "type": "select",
        "options": ["Yes", "No", "Not sure"]
    },
    {
        "id": "uk_support",
        "label": "Require UK-based support?",
        "type": "select",
        "options": ["Yes", "No", "Not sure"]
    }
]
