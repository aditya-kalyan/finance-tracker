import streamlit as st

def init_session():
    if "token" not in st.session_state:
        st.session_state.token = None
    if "email" not in st.session_state:
        st.session_state.email = None
