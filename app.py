import streamlit as st
from agent.core import JanusAgent
import agent.tools as tools
import agent.human_in_loop as human_in_loop
import os

st.set_page_config(page_title="Janus Agentic AI", layout="wide")
st.title("Janus Agentic AI")

# Agent Persona
persona_prompt = st.text_area("Agent Persona Prompt", value="You are an expert assistant working with the user.")

# File Upload
uploaded_files = st.file_uploader("Upload any files (images, docs, code, audio, etc.)", accept_multiple_files=True)
if uploaded_files:
    os.makedirs("uploads", exist_ok=True)
    for f in uploaded_files:
        with open(os.path.join("uploads", f.name), "wb") as out_f:
            out_f.write(f.getbuffer())

# Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("## Chat")
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

user_msg = st.chat_input(
    "Type your request here (e.g. 'Summarize my PDF', 'Generate an image of a rocket', 'Browse to google.com')")
if user_msg:
    st.session_state.chat_history.append({"role": "user", "content": user_msg})

    agent = JanusAgent(persona_prompt, tools, human_in_loop.approval_callback)
    plan = agent.parse_natural_language(user_msg, uploaded_files)

    st.markdown("### Agent Plan")
    for i, step in enumerate(plan):
        st.write(f"{i + 1}. Tool: `{step['tool']}` Args: `{step['args']}`")

    # Execute plan with approval for each step
    results = agent.execute_plan(plan)
    for result in results:
        st.session_state.chat_history.append({"role": "assistant", "content": str(result['result'])})
        if result['step']['tool'] == "image_generation" and result['result'] is not None:
            st.image(result['result'], caption="Generated Image")