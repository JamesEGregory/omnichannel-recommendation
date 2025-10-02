import streamlit as st
from questionnaires import QUESTIONS
from matcher import match_vendors

st.set_page_config(page_title="Omnichannel Contact Centre Recommender", layout="wide")

st.title("🏛️ Council Omnichannel Contact Centre Recommendation Tool")

st.markdown("""
Answer a few questions about your current environment and ambitions,
and we'll recommend the most suitable technology supplier based on our structured scoring model.
""")

# Collect questionnaire responses
responses = {}

st.header("📋 Questionnaire")

for q in QUESTIONS:
    qid = q["id"]
    qlabel = q["label"]
    qtype = q["type"]
    options = q.get("options", [])

    if qtype == "select":
        responses[qid] = st.selectbox(qlabel, [""] + options)
    elif qtype == "multiselect":
        responses[qid] = st.multiselect(qlabel, options)
    elif qtype == "text":
        responses[qid] = st.text_input(qlabel)
    else:
        st.warning(f"Unknown question type for {qid}")

# Submit button
if st.button("🔍 Get Recommendation"):
    st.subheader("🧠 Recommendation Engine Results")
    ranked, justification = match_vendors(responses)

    if ranked:
        top_vendor, top_score = ranked[0]
        st.success(f"🏆 **Recommended Supplier:** {top_vendor}  \n(Score: {top_score})")

        if len(ranked) > 1:
            st.markdown("**Other strong contenders:**")
            for vendor, score in ranked[1:4]:
                st.write(f"- {vendor} (Score: {score})")

        st.markdown(f"**Why this recommendation?**  \n{justification}")
    else:
        st.warning("No vendors could be matched — try filling more answers.")
