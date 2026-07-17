import streamlit as st

from utils.api import signup


st.title("📝 Create Account")


full_name = st.text_input(
    "Full Name",
    key="signup_full_name"
)

email = st.text_input(
    "Email",
    key="signup_email"
)

username = st.text_input(
    "Username",
    key="signup_username"
)

password = st.text_input(
    "Password",
    type="password",
    key="signup_password"
)


if st.button("Signup"):

    response = signup(
        {
            "full_name": full_name,
            "email": email,
            "username": username,
            "password": password
        }
    )


    if response.status_code == 200:

        st.success(
            "Account created successfully!"
        )

    else:

        st.error(
            response.text
        )