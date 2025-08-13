import streamlit as st
import json
from orchestrator import orchestrate

# Load config once
with open("pipeline_config.json") as f:
    config = json.load(f)

st.title("SynapseCore: Remote Agent Integration Hub")

st.markdown("""
Enter your message details below and see how the modular pipeline processes it step-by-step.
""")

user_id = st.text_input("User ID", value="abc123")
platform = st.selectbox("Platform", options=["instagram", "whatsapp", "email"])
message_text = st.text_area("Message Text", value="Did you finalize the pitch deck?")
timestamp = st.text_input("Timestamp (ISO format)", value="2025-08-05T13:00:00Z")

if st.button("Run Pipeline"):
    input_msg = {
        "user_id": user_id,
        "platform": platform,
        "message_text": message_text,
        "timestamp": timestamp
    }
    with st.spinner("Processing..."):
        output = orchestrate(input_msg, config)
    st.success("Pipeline completed!")

    st.subheader("Final Output")
    st.json(output)

    st.subheader("Logs Folder")
    st.write("Check the `logs/` directory for detailed stage logs saved as JSON.")

