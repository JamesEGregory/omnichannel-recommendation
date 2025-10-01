import streamlit as st
from questionnaires import DISCOVERY, DIAGNOSTIC
from vendor_loader import load_vendor_cards
from scoring import score_vendors

# ---------------------------
# App Layout
# ---------------------------
st.set_page_config(page_title="LocalGov CCaaS Advisor", layout="centered")

st.title("🏛 Local Government Contact Centre Technology Advisor")
st.markdown(
    """
    This tool helps councils determine the best-fit omni-channel contact centre technology.
    Answer a few questions and get tailored vendor recommendations based on your priorities,
    scale, infrastructure and strategic drivers.
    """
)

# ---------------------------
# Step 1: Questionnaire selection
# ---------------------------
st.sidebar.header("Questionnaire type")
questionnaire_type = st.sidebar.radio(
    "Choose which questionnaire to complete:",
    ("Discovery (early stage)", "Diagnostic (strategic)")
)

if questionnaire_type.startswith("Discovery"):
    questions = DISCOVERY
else:
    questions = DIAGNOSTIC

# ---------------------------
# Step 2: Render Questions
# ---------------------------
st.header("Step 1: Complete the questionnaire")

responses = {}

for q in questions:
    qid = q["id"]
    qtext = q["text"]
    qtype = q.get("type", "single")
    options = q.get("options", [])

    if qtype == "multi":
        responses[qid] = st.multiselect(qtext, options)
    elif qtype == "numeric":
        responses[qid] = st.number_input(qtext, min_value=0, step=1)
    elif qtype == "text":
        responses[qid] = st.text_input(q_text)
