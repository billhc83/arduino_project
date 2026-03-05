import streamlit as st
from data_base import verify_login
from utils.email_utils import send_temp_password

st.title("🛡️ Beginner Arduino Training")
st.subheader("Login to your Course")

with st.form("Login Form", border=True):
    user_input = st.text_input("Username")
    pass_input = st.text_input("Password", type="password")
    login_clicked = st.form_submit_button("Login", use_container_width=True, type="primary")

if login_clicked and user_input.strip() and pass_input.strip():
    clean_user = user_input.strip()
    clean_pass = pass_input.strip()
    user_data = verify_login(clean_user, clean_pass)
    if user_data:
        if not user_data.get("email_verified", False):
            st.error("📧 Please verify your email before logging in. Check your inbox.")
        else:
            st.session_state.is_admin = user_data.get("is_admin", False)
            st.session_state.is_parent = user_data.get("is_parent", False)
            st.session_state.user_id = clean_user
            st.toast("Welcome back!")
            st.rerun()
    else:
        st.error("Invalid username or password")

with st.expander("🔑 Forgot your password?"):
    st.caption(
        "If your account was created by a parent, "
        "ask them to reset your password from their Parent Dashboard."
    )
    forgot_email = st.text_input("Enter your email address", key="forgot_email")
    forgot_clicked = st.button("Send Temporary Password")
    if forgot_clicked:
        if not forgot_email or "@" not in forgot_email:
            st.error("Please enter a valid email address.")
        else:
            found = send_temp_password(forgot_email)
            if found:
                st.success("✅ A temporary password has been sent to your email.")
            else:
                st.error("No account found with that email address.")