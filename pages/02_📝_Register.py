import streamlit as st
from sqlalchemy import text
from data_base import conn, hash_password, notify_discord_new_request

st.title("📝 Create New Account")

with st.form("registration_form"):
    new_user = st.text_input("Choose a Username")
    new_pass = st.text_input("Choose a Password", type="password")
    confirm_pass = st.text_input("Repeat Password", type="password")
    
    submit = st.form_submit_button("Register")

    if submit:
        # 1. Basic validation
        if not new_user or not new_pass:
            st.error("Fields cannot be empty.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        else:
            # 2. Check if username exists
            existing_user = conn.query(
                "SELECT * FROM users WHERE username = :u",
                params={"u": new_user},
                ttl=0
            )
            
            if not existing_user.empty:
                st.error("Username already taken!")
            else:
                # 3. Save user in database
                try:
                    hashed = hash_password(new_pass)
                    with conn.session as s:
                        # First, add the profile to the public table
                        s.execute(
                            text(
                                "INSERT INTO public.users (username, is_approved, is_admin) "
                                "VALUES (:u, :a, :adm)"
                            ),
                            {"u": new_user, "a": False, "adm": False}
                        )
                        
                        # Second, add the password to the private table
                        s.execute(
                            text(
                                "INSERT INTO private.user_creds (username, password) "
                                "VALUES (:u, :p)"
                            ),
                            {"u": new_user, "p": hashed}
                        )
                        
                        # Commit both at once so it's "all or nothing"
                        s.commit()
                    
                    # 4. Notify Discord
                    notify_discord_new_request(new_user)
                    
                    st.success(
                        "✅ Registration successful! Your account is now pending admin approval."
                        " You will receive a notification when you can log in."
                    )

                    # Optional: redirect to login page automatically
                    # st.session_state.next_page = "Login"
                    # st.experimental_rerun()

                except Exception as e:
                    st.error(f"Error creating account: {e}")
