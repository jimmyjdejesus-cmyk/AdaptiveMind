import streamlit as st

def approval_callback(preview):
    st.markdown(f"### Next Action Preview\n{preview}")
    return st.button("Approve and Continue")