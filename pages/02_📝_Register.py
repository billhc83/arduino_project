import streamlit as st
from data_base import get_db_connection, hash_password

if "user_id" in st.session_state:
    keys_to_clear = ["user_id", "unlocked_pages", "last_user", "next_page"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    # Rerun to update the sidebar immediately
    st.rerun()

st.title("📝 Create New Account")

with st.form("registration_form"):
    new_user = st.text_input("Choose a Username")
    new_pass = st.text_input("Choose a Password", type="password")
    confirm_pass = st.text_input("Repeat Password", type="password")
    submit = st.form_submit_button("Register")

if submit:
    if not new_user or not new_pass:
        st.error("Fields cannot be empty.")
    elif new_pass != confirm_pass:
        st.error("Passwords do not match.")
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (new_user,))
        if cursor.fetchone():
            st.error("Username already taken!")
        else:
            # Save user
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                           (new_user, hash_password(new_pass)))
            conn.commit()
            st.success("Account created! Go back to the Home page to Login.")
