import streamlit as st
from data_base import verify_login, get_user_progress

st.title("🛡️ Beginner Arduino Training")
st.subheader("Login to your Course")

# Use a container for a clean layout
with st.container(border=True):
    user_input = st.text_input("Username")
    pass_input = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login", use_container_width=True, type="primary"):
            clean_user = user_input.strip()
            clean_pass = pass_input.strip()
            if verify_login(clean_user, clean_pass):
                st.session_state.user_id = user_input
                st.toast("Welcome back!") 
                st.rerun()
            else:
                # Put the error HERE, so it only shows if the login FAILS
                st.error("Invalid username or password")

                
    with col2:
        if st.button("Create Account", use_container_width=True):
            # Use the trigger variable we set up in main.py
            st.session_state.next_page = "Register"
            st.rerun()

st.divider()

# Only show "Current Progress" if logged in
if "user_id" in st.session_state:
    st.info(f"Welcome back, **{st.session_state.user_id}**!")
    st.write(f"You have unlocked: {', '.join(st.session_state.unlocked_pages)}")

if "user_id" in st.session_state:
    st.divider()
    if st.button("Log Out 🚪", type="secondary", use_container_width=True):
        # Clear the specific keys used for tracking
        keys_to_clear = ["user_id", "unlocked_pages", "last_user", "next_page"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        # Trigger a rerun so main.py resets the sidebar to Guest mode
        st.rerun()