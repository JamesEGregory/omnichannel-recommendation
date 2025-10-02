import streamlit as st
from questionnaires import DIAGNOSTIC
from gpt_client import get_recommendation

# -----------------------------------------
# App header
# -----------------------------------------
st.title("Omnichannel Contact Centre Recommendation Tool")

st.markdown("""
This tool helps councils identify the most suitable contact centre platform 
based on theirimport streamlit as st
from questionnaires import DIAGNOSTIC
from gpt_client import get_recommendation

# -----------------------------------------
# App header
# -----------------------------------------
st.title("Omnichannel Contact Centre Recommendation Tool")

st.markdown("""
This tool helps councils identify the most suitable contact centre platform 
based on their scale, priorities, infrastructure, and channel strategy.
""")

# -----------------------------------------
# Questionnaire rendering (DIAGNOSTIC only)
# -----------------------------------------
st.header("Diagnostic Questionnaire")

questionnaire = DIAGNOSTIC
responses = {}

for q in questionnaire:
    qid = q["id"]
    qlabel = q.get("label") or q.get("text")  # supports both naming styles
    qtype = q.get("type")

    if qtype == "multiselect":
        responses[qid] = st.multiselect(qlabel, q.get("options", []))
    elif qtype == "select":
        responses[qid] = st.selectbox(qlabel, [""] + q.get("options", []))  # allow blank
    else:
        responses[qid] = st.text_input(qlabel)

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
                st.markdown(f"**Secondary option:** {recommendation['secondary_vendor']}")

            st.subheader("Rationale")
            st.write(recommendation["justification"])

            st.subheader("Cost Estimate")
            st.write(f"💰 Estimated cost per agent: £{recommendation['cost_per_agent']}/month")
            st.write(f"📊 Estimated total monthly cost: £{recommendation['total_cost']}")

            if "savings" in recommendation:
                st.write(f"💡 Estimated monthly savings: £{recommendation['savings']}")

        except Exception as e:
            st.error(f"An error occurred while generating recommendation: {e}")
 scale, priorities, infrastructure, and channel strategy.
""")

# -----------------------------------------
# Questionnaire rendering (DIAGNOSTIC only)
# -----------------------------------------
st.header("Diagnostic Questionnaire")

questionnaire = DIAGNOSTIC
responses = {}

for q in questionnaire:
    qid = q["id"]
    qlabel = q.get("label") or q.get("text")

    if q.get("type") == "multiselect":
        responses[qid] = st.multiselect(qlabel, q["options"])
    elif q.get("type") == "select":
        responses[qid] = st.selectbox(qlabel, [""] + q["options"])  # allow blank
    else:
        responses[qid] = st.text_input(label)

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
                st.markdown(f"**Secondary option:** {recommendation['secondary_vendor']}")

            st.subheader("Rationale")
            st.write(recommendation["justification"])

            st.subheader("Cost Estimate")
            st.write(f"💰 Estimated cost per agent: £{recommendation['cost_per_agent']}/month")
            st.write(f"📊 Estimated total monthly cost: £{recommendation['total_cost']}")

            if "savings" in recommendation:
                st.write(f"💡 Estimated monthly savings: £{recommendation['savings']}")

        except Exception as e:
            st.error(f"An error occurred while generating recommendation: {e}")
