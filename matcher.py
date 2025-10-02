import yaml
import glob
import os

# ---------------------------------------
# Scoring weightings by pillar
# ---------------------------------------
WEIGHTS = {
    "scale": 0.15,
    "integration": 0.25,
    "automation": 0.15,
    "commercial": 0.15,
    "channel": 0.15,
    "deployment": 0.10,
    "strategy": 0.05
}

# ---------------------------------------
# Load vendor YAML files
# ---------------------------------------
def load_vendors():
    vendors = []
    for file in glob.glob(os.path.join("vendors", "*.yaml")):
        with open(file, "r") as f:
            vendors.append(yaml.safe_load(f))
    return vendors


# ---------------------------------------
# Helper: Scale match
# ---------------------------------------
def score_scale(vendor, answers):
    agents = answers.get("agents")
    if not agents:
        return 0

    scale_text = vendor["sweet_spot"]["scale"].lower()
    if "small" in scale_text and agents == "<20":
        return 1
    if "mid" in scale_text and agents in ["20–100", "100–300"]:
        return 1
    if "large" in scale_text and agents == "300+":
        return 1
    return 0


# ---------------------------------------
# Helper: Integration match
# ---------------------------------------
def score_integration(vendor, answers):
    score = 0

    # Telephony
    tel = answers.get("telephony")
    tel_supported = vendor.get("integrations", {}).get("telephony", {})
    if tel and any(tel.lower() in str(v).lower() for v in tel_supported.values()):
        score += 1

    # CRM
    crm = answers.get("crm")
    crm_supported = vendor.get("integrations", {}).get("crm", {}).get("supported", [])
    if crm and any(crm.lower() in c.lower() for c in crm_supported):
        score += 1

    # Back-office connectors
    bo_systems = answers.get("back_office_systems", [])
    vendor_bo = vendor.get("integrations", {}).get("back_office", {}).get("typical", [])
    if bo_systems:
        overlap = len(set(bo_systems) & set(vendor_bo))
        if overlap > 0:
            score += min(1, overlap / len(bo_systems))  # cap at 1

    return score


# ---------------------------------------
# Helper: Automation depth
# ---------------------------------------
def score_automation(vendor, answers):
    ambition = answers.get("automation_extent")
    if not ambition:
        return 0

    depth = vendor.get("automation_depth", {})
    if ambition == "Switchboard only":
        return 1 if depth.get("switchboard") else 0
    if ambition == "Service Requests":
        return 1 if depth.get("service_requests") else 0
    if ambition == "Transactions":
        return 1 if depth.get("transactions") else 0
    if ambition == "Complex Assessments":
        return 1 if depth.get("complex_agentic") else 0
    return 0


# ---------------------------------------
# Helper: Commercials
# ---------------------------------------
def score_commercial(vendor, answers):
    budget = answers.get("budget")
    pricing = vendor.get("commercials", {}).get("pricing_band", "").lower()
    if not budget or not pricing:
        return 0

    budget = budget.lower()
    if budget == "low" and "low" in pricing:
        return 1
    if budget == "medium" and ("low" in pricing or "mid" in pricing):
        return 1
    if budget == "high":
        return 1  # assume all work for high budget
    return 0


# ---------------------------------------
# Helper: Channel coverage
# ---------------------------------------
def score_channel(vendor, answers):
    desired_channels = answers.get("channels_now", [])
    if not desired_channels:
        return 0

    vendor_channels = vendor.get("channels", {})
    match_count = 0

    for ch in desired_channels:
        ch_key = ch.lower()
        if ch_key in vendor_channels and vendor_channels[ch_key]:
            match_count += 1

    return match_count / len(desired_channels)  # proportion matched


# ---------------------------------------
# Helper: Deployment
# ---------------------------------------
def score_deployment(vendor, answers):
    urgency = answers.get("urgency")
    time_to_deploy = vendor.get("commercials", {}).get("time_to_deploy", "").lower()

    if not urgency or not time_to_deploy:
        return 0

    if urgency == "<3 months" and "fast" in time_to_deploy:
        return 1
    if urgency == "3–6 months" and ("fast" in time_to_deploy or "medium" in time_to_deploy):
        return 1
    if urgency in ["6–12 months", "12+ months"]:
        return 1  # any vendor works if timeline is long
    return 0


# ---------------------------------------
# Helper: Strategy fit
# ---------------------------------------
def score_strategy(vendor, answers):
    priorities = answers.get("priorities", [])
    strength = vendor.get("main_strength", "").lower()

    if not priorities or not strength:
        return 0

    score = 0
    for p in priorities:
        if p.lower() in strength:
            score += 1

    return min(1, score / len(priorities))


# ---------------------------------------
# Main: match vendors
# ---------------------------------------
def match_vendors(answers):
    vendors = load_vendors()
    scored = []

    for vendor in vendors:
        s = 0
        s += WEIGHTS["scale"] * score_scale(vendor, answers)
        s += WEIGHTS["integration"] * score_integration(vendor, answers)
        s += WEIGHTS["automation"] * score_automation(vendor, answers)
        s += WEIGHTS["commercial"] * score_commercial(vendor, answers)
        s += WEIGHTS["channel"] * score_channel(vendor, answers)
        s += WEIGHTS["deployment"] * score_deployment(vendor, answers)
        s += WEIGHTS["strategy"] * score_strategy(vendor, answers)

        scored.append((vendor["name"], round(s, 3)))

    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)

    # Build justification for top vendor
    top_vendor = scored[0][0] if scored else None
    justification = ""
    if top_vendor:
        justification = f"{top_vendor} is the best fit based on your scale, integration landscape, and priorities."

    return scored, justification
