import streamlit as st
from utils.api import login

st.title("🔐 Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):

    response = login(email, password)

    if response.status_code == 200:

        token = response.json()["access_token"]

        st.session_state["token"] = token

        st.success("Login Successful!")

        st.switch_page("pages/dashboard.py")

    else:
        st.error("Invalid email or password")