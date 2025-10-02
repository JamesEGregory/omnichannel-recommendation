# questionnaires.py

QUESTIONS = [
    # 1. Scale & Operating Model
    {"id": "agents", "label": "Approx. number of agents in your contact centre", "type": "select",
     "options": ["<20", "20–100", "100–300", "300+"]},

    {"id": "structure", "label": "How are your teams structured?", "type": "select",
     "options": ["Single central centre", "Multiple departmental teams", "Mixed", "Not sure"]},

    {"id": "contact_volume", "label": "Annual inbound contact volume (all channels)", "type": "select",
     "options": ["<50k", "50k–250k", "250k–1m", "1m+"]},

    # 2. Channel Mix & Pain Points
    {"id": "channels_now", "label": "Which channels are currently in use?", "type": "multiselect",
     "options": ["Voice", "Webchat", "Email", "SMS", "Social", "Self-service portal", "In-person"]},

    {"id": "channel_pain", "label": "Which channels cause the most pain?", "type": "select",
     "options": ["Voice", "Email", "Webchat", "Social", "Self-service portal", "None", "Not sure"]},

    {"id": "top_services", "label": "Top service areas for inbound contact", "type": "text"},

    # 3. Infrastructure & Integration
    {"id": "telephony", "label": "Current telephony platform", "type": "select",
     "options": ["Avaya", "Cisco", "Mitel", "Teams Voice", "8x8", "RingCentral", "Other"]},

    {"id": "crm", "label": "CRM or case management system", "type": "select",
     "options": ["Dynamics 365", "Salesforce", "Netcall Liberty", "Civica", "Capita ONE", "ServiceNow", "None/Unknown"]},

    {"id": "back_office", "label": "Which back-office systems do you rely on most?", "type": "multiselect",
     "options": [
         "Revenues & Benefits",
         "Waste Management",
         "Housing",
         "Environmental Health",
         "Planning/Building Control",
         "Highways",
         "Other"
     ]},

    {"id": "it_capacity", "label": "Internal IT/developer capacity", "type": "select",
     "options": ["Low", "Medium", "High", "Not sure"]},

    {"id": "expected_spend", "label": "Expected annual spend on telephony/contact centre solutions", "type": "select",
     "options": ["<£50k", "£50k–£150k", "£150k–£500k", "£500k+", "Not sure"]},

    # 4. Ambition & Strategy
    {"id": "priorities", "label": "Top priorities for transformation", "type": "multiselect",
     "options": ["Cost savings", "Improve CX", "Channel expansion", "Upgrade telephony", "Integration/workflow", "Resilience/BCP"]},

    {"id": "automation", "label": "How ambitious are you with automation?", "type": "select",
     "options": ["Switchboard only", "Service Requests", "Transactions", "Complex agentic automation"]},

    {"id": "timeline", "label": "Target go-live timeline", "type": "select",
     "options": ["<3 months", "3–6 months", "6–12 months", "12+ months"]},

    {"id": "channel_strategy", "label": "How clear is your channel strategy or roadmap?", "type": "select",
     "options": ["Very clear", "Partially defined", "Early thinking", "Not started"]},

    # 5. Leadership & Org
    {"id": "leadership_engagement", "label": "How engaged is leadership in contact centre transformation?", "type": "select",
     "options": ["Strongly", "Moderately", "Lightly", "Not yet"]},

    {"id": "governance", "label": "Is there a clear sponsorship or governance structure?", "type": "select",
     "options": ["Yes", "Partial", "No", "Not sure"]},

    {"id": "platform_ownership", "label": "Who will own the platform day-to-day?", "type": "select",
     "options": ["Corporate IT", "Customer Services", "Mixed", "Not yet decided"]},

    {"id": "platform_consolidation", "label": "How willing are you to consider platform consolidation (e.g. telephony + CCaaS)?", "type": "select",
     "options": ["Very", "Somewhat", "Not at all"]},
]
