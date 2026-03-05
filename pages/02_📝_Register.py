import streamlit as st
from sqlalchemy import text
from data_base import conn
from utils.auth_utils import hash_password
from utils.email_utils import send_verification_email

st.title("📝 Create Account")

with st.form("registration_form"):
    new_user = st.text_input("Choose a Username")
    email = st.text_input("Email Address")
    new_pass = st.text_input("Choose a Password", type="password")
    confirm_pass = st.text_input("Repeat Password", type="password")

    account_type = st.radio(
        "Account Type",
        options=["Select an account type", "I am a User", "I am a Parent"],
        index=0,
        help=(
            "User: You will use the app directly.\n\n"
            "Parent: You will create and manage accounts for your children. "
            "You will not use the app directly."
        )
    )

    submit = st.form_submit_button("Register")

if submit:
    if not new_user or not new_pass or not email:
        st.error("All fields are required.")
    elif account_type == "Select an account type":
        st.error("Please select an account type.")
    elif new_pass != confirm_pass:
        st.error("Passwords do not match.")
    elif "@" not in email or "." not in email:
        st.error("Please enter a valid email address.")
    else:
        existing_user = conn.query(
            "SELECT username FROM public.users WHERE LOWER(username) = LOWER(:u)",
            params={"u": new_user},
            ttl=0
        )
        existing_email = conn.query(
            "SELECT email FROM public.users WHERE LOWER(email) = LOWER(:e)",
            params={"e": email},
            ttl=0
        )

        if not existing_user.empty:
            st.error("Username already taken.")
        elif not existing_email.empty:
            st.error("An account with that email already exists.")
        else:
            try:
                is_parent = account_type == "I am a Parent"
                hashed = hash_password(new_pass)

                with conn.session as s:
                    s.execute(
                        text("""
                            INSERT INTO public.users 
                                (username, email, is_approved, is_admin, is_parent, email_verified, max_children)
                            VALUES 
                                (:u, :e, :a, :adm, :parent, :verified, :max_children)
                        """),
                        {
                            "u": new_user,
                            "e": email,
                            "a": False,
                            "adm": False,
                            "parent": is_parent,
                            "verified": False,
                            "max_children": 3 if is_parent else 0
                        }
                    )
                    s.execute(
                        text("""
                            INSERT INTO private.user_creds (username, password)
                            VALUES (:u, :p)
                        """),
                        {"u": new_user, "p": hashed}
                    )
                    s.commit()

                send_verification_email(new_user, email)
                st.success("✅ Account created! Please check your email to verify your account before logging in.")

            except Exception as e:
                st.error(f"Error creating account: {e}")