# questionnaires.py

DISCOVERY = [
    {"id": "agents", "text": "Approx. number of agents", "type": "select",
     "options": ["<20", "20–100", "100–300", "300+"]},
    {"id": "structure", "text": "How are teams structured?", "type": "select",
     "options": ["Single central centre", "Multiple departmental teams", "Mixed", "Not sure"]},
    {"id": "channels_now", "text": "Channels in use (select all)", "type": "multiselect",
     "options": ["Voice", "Webchat", "Email", "SMS", "Social", "Self-service portal", "In-person"]},
    {"id": "channel_pain", "text": "Which channel causes most pain?", "type": "select",
     "options": ["Voice", "Email", "Webchat", "Social", "Not sure"]},
    {"id": "top_services", "text": "Top interaction drivers (free text)", "type": "text"},
    {"id": "telephony", "text": "Telephony estate", "type": "select",
     "options": ["Avaya", "Cisco", "Mitel", "Teams Voice", "8x8", "RingCentral", "Other/Unknown"]},
    {"id": "crm", "text": "CRM/case management", "type": "select",
     "options": ["Dynamics 365", "Salesforce", "Netcall Liberty", "Civica", "Capita ONE", "ServiceNow", "None/Unknown"]},
    {"id": "self_service", "text": "Self-service/portal adoption", "type": "select",
     "options": ["None/basic", "Some services", "Widely used", "Not sure"]},
    {"id": "pain_points", "text": "Biggest operational pain (select up to 3)", "type": "multiselect",
     "options": ["Long queues", "Multi-channel demand mgmt", "Poor integration", "Limited automation",
                 "Inconsistent CX", "Aging PBX", "Weak MI/analytics"]},
    {"id": "priorities", "text": "Top 2–3 priorities", "type": "multiselect",
     "options": ["Cost savings", "Improve CX", "Channel expansion", "Upgrade telephony", "Integration/workflow",
                 "Resilience/BCP"]},
    {"id": "it_capacity", "text": "Internal IT/dev capacity", "type": "select",
     "options": ["Low", "Medium", "High", "Not sure"]},
    {"id": "budget", "text": "Budget band (run + change)", "type": "select",
     "options": ["Low", "Medium", "High", "Unknown"]},
    {"id": "urgency", "text": "Target go-live timescale", "type": "select",
     "options": ["<3 months", "3–6 months", "6–12 months", "12+ months"]},
    {"id": "security", "text": "Security/sovereignty driver", "type": "select",
     "options": ["Yes", "No", "Not sure"]},
    {"id": "uk_support", "text": "Require UK-based support?", "type": "select",
     "options": ["Yes", "No", "Not sure"]},
]

DIAGNOSTIC = [
    # Scale & structure (sizing)
    {"id": "agents", "text": "Approx. number of agents", "type": "select",
     "options": ["<20", "20–100", "100–300", "300+"]},
    {"id": "structure", "text": "How are teams structured?", "type": "select",
     "options": ["Single central centre", "Multiple departmental teams", "Mixed", "Not sure"]},
    {"id": "complexity", "text": "Service complexity (typical cases)", "type": "select",
     "options": ["Simple enquiries", "Mixed enquiries & requests", "Transactions", "Complex assessments"]},
    {"id": "volume_profile", "text": "Demand profile", "type": "select",
     "options": ["Steady", "Moderate peaks (seasonal)", "High peaks (tax/waste/etc.)", "Unknown"]},

    # Current estate (telephony/CC/CRM/WEM)
    {"id": "telephony", "text": "Current telephony/PBX or cloud voice", "type": "select",
     "options": ["Avaya", "Cisco", "Mitel", "Teams Voice", "8x8", "RingCentral", "Content Guru (storm)", "Other/Unknown"]},
    {"id": "cc_platform", "text": "Current contact centre platform (if any)", "type": "select",
     "options": ["None", "Genesys", "AWS Connect", "Talkdesk", "Five9", "NICE CXone", "Content Guru", "Zoom CC", "Netcall", "Other/Unknown"]},
    {"id": "crm", "text": "Primary CRM / case management", "type": "select",
     "options": ["Dynamics 365", "Salesforce", "Netcall Liberty", "Civica", "Capita ONE", "ServiceNow", "None/Unknown"]},
    {"id": "wem", "text": "WEM/WFM approach today", "type": "select",
     "options": ["Native in CC platform", "Third-party WEM", "Basic spreadsheets", "Unknown"]},

    # Channel mix & self-service
    {"id": "channels_now", "text": "Channels in use (select all)", "type": "multiselect",
     "options": ["Voice", "Webchat", "Email", "SMS", "Social", "WhatsApp", "Self-service portal", "In-person"]},
    {"id": "self_service", "text": "Self-service/portal adoption", "type": "select",
     "options": ["None/basic", "Some services", "Widely used", "Not sure"]},
    {"id": "channel_pain", "text": "Which channel causes most pain?", "type": "select",
     "options": ["Voice", "Email", "Webchat", "Social/WhatsApp", "Not sure"]},

    # Integrations & data
    {"id": "integration", "text": "Integration maturity", "type": "select",
     "options": ["Manual/siloed", "Point-to-point", "Middleware/APIs", "Mature integration platform"]},
    {"id": "back_office", "text": "Priority back-office systems to integrate (free text)", "type": "text"},
    {"id": "data_residency", "text": "Data residency requirement", "type": "select",
     "options": ["UK only", "UK/EU", "No strict requirement", "Unsure"]},

    # Strategy & priorities
    {"id": "strategy", "text": "Top strategic drivers (pick up to 3)", "type": "multiselect",
     "options": ["Cost savings", "Channel shift", "CX improvement", "WEM/workforce",
                 "Resilience/BCP", "Data/insight", "Automation/AI"]},
    {"id": "automation", "text": "Automation ambition (3-year horizon)", "type": "select",
     "options": ["Switchboard", "Service requests", "Transactions", "Complex/agentic (front-to-back)"]},
    {"id": "omni", "text": "Channel strategy", "type": "select",
     "options": ["Voice-first + digital", "Digital-first", "True omni-channel orchestration"]},
    {"id": "hand_off", "text": "Seamless cross-channel hand-off required?", "type": "select",
     "options": ["Yes", "No", "Not sure"]},

    # Constraints & preferences
    {"id": "delivery", "text": "Delivery capacity preference", "type": "select",
     "options": ["Turnkey vendor", "Hybrid (partner + in-house)", "Open platform we control"]},
    {"id": "procurement", "text": "Commercial model preference", "type": "select",
     "options": ["Subscription (per agent/month)", "Consumption (pay per use)", "CapEx", "No preference"]},
    {"id": "lock_in", "text": "Avoid vendor lock-in?", "type": "select",
     "options": ["Not a concern", "Important", "Critical"]},
    {"id": "ms_bias", "text": "Microsoft stack bias (Teams/D365)?", "type": "select",
     "options": ["Yes", "No", "Mixed/Unsure"]},
    {"id": "security", "text": "Security/sovereignty driver present?", "type": "select",
     "options": ["Yes", "No", "Not sure"]},
    {"id": "uk_support", "text": "Require UK-based support?", "type": "select",
     "options": ["Yes", "No", "Not sure"]},

    # Budget, capacity, urgency
    {"id": "budget", "text": "Budget band (run + change)", "type": "select",
     "options": ["Low", "Medium", "High", "Unknown"]},
    {"id": "it_capacity", "text": "Internal IT/dev capacity", "type": "select",
     "options": ["Low", "Medium", "High", "Not sure"]},
    {"id": "urgency", "text": "Target go-live timescale", "type": "select",
     "options": ["<3 months", "3–6 months", "6–12 months", "12+ months"]},

    # Operational pain & outcomes
    {"id": "pain_points", "text": "Biggest operational pain (select up to 3)", "type": "multiselect",
     "options": ["Long queues", "Multi-channel demand mgmt", "Poor integration", "Limited automation",
                 "Inconsistent CX", "Aging PBX", "Weak MI/analytics"]},
    {"id": "kpis", "text": "Priority outcomes/KPIs", "type": "multiselect",
     "options": ["Reduce cost-to-serve", "Increase containment", "Improve FCR",
                 "Lower ASA/abandonment", "Improve CSAT", "Shift to digital/self-serve"]},
]
