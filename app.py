import streamlit as st
from questionnaires import DISCOVERY, DIAGNOSTIC
from gpt_client import get_recommendation
from vendor_loader import load_vendor_cards

# -----------------------------------------
# Sidebar for choosing questionnaire type
# -----------------------------------------
st.sidebar.title("Settings")
questionnaire_type = st.sidebar.radio(
    "Choose questionnaire type:",
    ("Diagnostic", "Discovery"),  # ✅ Diagnostic first
    index=0                       # ✅ Default to Diagnostic
)

# Select which questionnaire to use
if questionnaire_type == "Discovery":
    questionnaire = DISCOVERY
else:
    questionnaire = DIAGNOSTIC

# -----------------------------------------
# Load vendor YAMLs
# -----------------------------------------
try:
    vendors = load_vendor_cards("vendors")
    print(f"✅ Loaded {len(vendors)} vendor profiles: {list(vendors.keys())}")
except Exception as e:
    print(f"❌ Failed to load vendor YAMLs: {e}")
    vendors = {}

# -----------------------------------------
# Page title and intro
# -----------------------------------------
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
    qtext = q["label"]  # ✅ Using label now

    qtype = q.get("type", "text")

    if qtype == "multiselect":
        responses[qid] = st.multiselect(qtext, q.get("options", []))
    elif qtype == "select":
        responses[qid] = st.selectbox(qtext, [""] + q.get("options", []))  # allow blank
    else:
        responses[qid] = st.text_input(qtext)

# -----------------------------------------
# Recommendation trigger
# -----------------------------------------
if st.button("Get Recommendation"):
    with st.spinner("Generating recommendation..."):
        try:
            recommendation = get_recommendation(responses)
            st.success("Recommendation generated successfully ✅")

            st.subheader("Top Vendor Recommendation")
            st.markdown(f"**{recommendation['primary_vendor']}**")

            if "secondary_vendor" in recommendation:
                st.markdown(
                    f"**Secondary option:** {recommendation['secondary_vendor']}"
                )

            st.subheader("Rationale")
            st.write(recommendation.get("justification", "No detailed rationale returned."))

            if "cost_per_agent" in recommendation:
                st.subheader("Cost Estimate")
                st.write(f"💰 Estimated cost per agent: £{recommendation['cost_per_agent']}/month")
                st.write(f"📊 Estimated total monthly cost: £{recommendation.get('total_cost', 'N/A')}")

            if "savings" in recommendation:
                st.write(f"💡 Estimated monthly savings: £{recommendation['savings']}")

        except Exception as e:
            st.error(f"An error occurred while generating recommendation: {e}")
