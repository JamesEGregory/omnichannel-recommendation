import streamlit as st
from questionnaires import DISCOVERY, DIAGNOSTIC
from gpt_client import get_recommendation
from vendor_loader import load_vendor_cards

# -----------------------------
# Load vendor YAML profiles
# -----------------------------
try:
    vendors = load_vendor_cards("vendors")  # looks inside /vendors folder
    print(f"✅ Loaded {len(vendors)} vendor profiles: {list(vendors.keys())}")
except Exception as e:
    print(f"❌ Failed to load vendor YAMLs: {e}")
    vendors = {}

# -----------------------------------------
# Sidebar for choosing questionnaire type
# -----------------------------------------
st.sidebar.title("Settings")
questionnaire_type = st.sidebar.radio(
    "Choose questionnaire type:",
    ("Discovery", "Diagnostic")
)

# Select which questionnaire to use
if questionnaire_type == "Discovery":
    questionnaire = DISCOVERY
else:
    questionnaire = DIAGNOSTIC

st.title("Omnichannel Contact Centre Recommendation Tool")

st.markdown("""
This tool helps councils identify the most suitable contact centre platform based on 
their scale, priorities, infrastructure, and channel strategy.
""")

# -----------------------------------------
# Questionnaire rendering
# -----------------------------------------
st.header(f"{questionnaire_type} Questionnaire")

responses = {}

for q in questionnaire:
    qid = q["id"]
    qtext = q["text"]  # ✅ Important: we're using "label" now

    qtype = q.get("type", "text")
    options = q.get("options", [])

    if qtype == "multiselect":
        responses[qid] = st.multiselect(qtext, options)
    elif qtype == "select":
        responses[qid] = st.selectbox(qtext, [""] + options)
    else:
        responses[qid] = st.text_input(qtext)

# -----------------------------------------
# Recommendation trigger
# -----------------------------------------
if st.button("Get Recommendation"):
    with st.spinner("Generating recommendation..."):
        try:
            recommendation = get_recommendation(responses, vendors)
            st.success("Recommendation generated successfully ✅")

            st.subheader("Top Vendor Recommendation")
            st.markdown(f"**{recommendation['primary_vendor']}**")

            if "secondary_vendor" in recommendation:
                st.markdown(
                    f"**Secondary option:** {recommendation['secondary_vendor']}"
                )

            st.subheader("Rationale")
            st.write(recommendation["justification"])

            if "cost_per_agent" in recommendation:
                st.subheader("Cost Estimate")
                st.write(f"💰 Estimated cost per agent: £{recommendation['cost_per_agent']}/month")
                st.write(f"📊 Estimated total monthly cost: £{recommendation['total_cost']}")

            if "savings" in recommendation:
                st.write(f"💡 Estimated monthly savings: £{recommendation['savings']}")

        except Exception as e:
            st.error(f"An error occurred while generating recommendation: {e}")
