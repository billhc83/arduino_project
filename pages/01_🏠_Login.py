import streamlit as st
from data_base import verify_login

st.title("🛡️ Beginner Arduino Training")
st.subheader("Login to your Course")

with st.form("Login Form", border=True):
    user_input = st.text_input("Username")
    pass_input = st.text_input("Password", type="password")
    login_clicked = st.form_submit_button("Login", use_container_width=True, type="primary")

    if login_clicked:
        clean_user = user_input.strip()
        clean_pass = pass_input.strip()
        user_data = verify_login(clean_user, clean_pass)
        if user_data:
            if not user_data.get("is_approved", False):
                st.error("🚨 Your account is pending approval.")
            elif user_data.get("is_parent") and not user_data.get("email_verified", False):
                st.error("📧 Please verify your email before logging in. Check your inbox.")
            else:
                st.session_state.is_admin = user_data.get("is_admin", False)
                st.session_state.is_parent = user_data.get("is_parent", False)
                st.session_state.user_id = clean_user
                st.toast("Welcome back!")
                st.rerun()
        else:
            st.error("Invalid username or password")

st.divider()

# Optional: show current progress only if logged in
if st.session_state.get("user_id"):
    st.info(f"Welcome back, **{st.session_state.user_id}**!")
    st.write(f"You have unlocked: {', '.join(st.session_state.get('unlocked_pages', []))}")
