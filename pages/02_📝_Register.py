import streamlit as st
from data_base import hash_password

if "user_id" in st.session_state:
    keys_to_clear = ["user_id", "unlocked_pages", "last_user", "next_page"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    # Rerun to update the sidebar immediately
    st.rerun()

st.title("📝 Create New Account")

import streamlit as st
from sqlalchemy import text
from data_base import conn, hash_password # Import our cloud connection and hasher

st.title("Create an Account")

with st.form("registration_form"):
    new_user = st.text_input("Choose a Username")
    new_pass = st.text_input("Choose a Password", type="password")
    confirm_pass = st.text_input("Repeat Password", type="password")
    
    # --- JOIN CODE ADDED HERE ---
    join_code = st.text_input("Enter the Arduino Club Join Code", type="password")
    
    submit = st.form_submit_button("Register")

if submit:
    # 1. Check Join Code first (Bot/Stranger protection)
    # We will set 'arduino2025' as the code in secrets.toml later
    correct_code = st.secrets.get("JOIN_CODE", "dev_default")
    
    if join_code != correct_code:
        st.error("Incorrect Join Code. Please contact the administrator.")
    
    # 2. Basic validation
    elif not new_user or not new_pass:
        st.error("Fields cannot be empty.")
    elif new_pass != confirm_pass:
        st.error("Passwords do not match.")
        
    else:
        # 3. Check if username exists (The Supabase Way)
        existing_user = conn.query(
            "SELECT * FROM users WHERE username = :u",
            params={"u": new_user},
            ttl=0
        )
        
        if not existing_user.empty:
            st.error("Username already taken!")
        else:
            # 4. Save user using conn.session
            try:
                hashed = hash_password(new_pass)
                with conn.session as s:
                    s.execute(
                        text("INSERT INTO users (username, password) VALUES (:u, :p)"),
                        {"u": new_user, "p": hashed}
                    )
                    s.commit()
                st.success("Account created! You can now log in.")
            except Exception as e:
                st.error(f"Error creating account: {e}")
