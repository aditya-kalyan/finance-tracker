import streamlit as st
from utils.auth import login, register
from utils.session import init_session

st.set_page_config(page_title="Budget Tracker", layout="centered")
init_session()

st.title("💸 Budget Tracker")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        result = login(email, password)
        if result:
            data = result.json()
            st.session_state.token = data["access_token"]
            st.success("Login successful!")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Invalid credentials" + result.text)

with tab2:
    email = st.text_input("New Email")
    password = st.text_input("New Password", type="password")
    if st.button("Register"):
        res = register(email, password)
        if res.status_code == 200:
            st.success("Registered! Please login.")
        else:
            st.error(res.json().get("detail", "Registration failed"))
