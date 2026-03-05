import streamlit as st
from sqlalchemy import text
from data_base import conn
from utils.auth_utils import hash_password

st.title("👨‍👩‍👧 Parent Dashboard")

if not st.session_state.get("user_id"):
    st.error("You must be logged in to view this page.")
    st.stop()

parent_username = st.session_state.user_id

# fetch parent info
parent_data = conn.query(
    "SELECT email, max_children FROM public.users WHERE LOWER(username) = LOWER(:u)",
    params={"u": parent_username},
    ttl=0
)

if parent_data.empty:
    st.error("Could not load account data.")
    st.stop()

max_children = parent_data.iloc[0]["max_children"]
email = parent_data.iloc[0]["email"]

# fetch existing child accounts
children = conn.query(
    """
    SELECT cp.username, cp.display_name 
    FROM public.child_profiles cp
    WHERE cp.parent_username = :u
    ORDER BY cp.created_at ASC
    """,
    params={"u": parent_username},
    ttl=0
)

child_count = len(children)

# ------------------------------------------------
# Section 1 — Child Accounts
# ------------------------------------------------
st.subheader("👧 Child Accounts")
st.caption(f"You have {child_count} of {max_children} child accounts created.")

if not children.empty:
    for _, child in children.iterrows():
        with st.expander(f"👤 {child['username']}"):
            
            # reset password
            st.markdown("**Reset Password**")
            new_pass = st.text_input(
                "New Password", 
                type="password", 
                key=f"pass_{child['username']}"
            )
            confirm_pass = st.text_input(
                "Confirm Password", 
                type="password", 
                key=f"confirm_{child['username']}"
            )
            if st.button("Update Password", key=f"update_{child['username']}"):
                if not new_pass:
                    st.error("Password cannot be empty.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                else:
                    hashed = hash_password(new_pass)
                    with conn.session as s:
                        s.execute(
                            text("""
                                UPDATE private.user_creds 
                                SET password = :p 
                                WHERE LOWER(username) = LOWER(:u)
                            """),
                            {"p": hashed, "u": child["username"]}
                        )
                        s.commit()
                    st.success(f"✅ Password updated for {child['username']}.")

            st.divider()

            # delete account
            st.markdown("**Delete Account**")
            st.warning(f"This will permanently delete **{child['username']}** and all their progress.")
            if st.button("🗑️ Delete Account", key=f"delete_{child['username']}"):
                with conn.session as s:
                    s.execute(
                        text("DELETE FROM private.user_creds WHERE LOWER(username) = LOWER(:u)"),
                        {"u": child["username"]}
                    )
                    s.execute(
                        text("DELETE FROM public.child_profiles WHERE LOWER(username) = LOWER(:u)"),
                        {"u": child["username"]}
                    )
                    s.commit()
                st.success(f"✅ {child['username']} has been deleted.")
                st.rerun()
else:
    st.info("You have no child accounts yet. Create one below.")

# ------------------------------------------------
# Section 2 — Create Child Account
# ------------------------------------------------
if child_count < max_children:
    st.subheader("➕ Create Child Account")
    with st.form("create_child_form"):
        child_username = st.text_input("Username")
        child_pass = st.text_input("Password", type="password")
        child_confirm = st.text_input("Confirm Password", type="password")
        create = st.form_submit_button("Create Account")

    if create:
        if not child_username or not child_pass:
            st.error("All fields are required.")
        elif child_pass != child_confirm:
            st.error("Passwords do not match.")
        else:
            # check username not taken globally
            existing = conn.query(
                """
                SELECT username FROM public.users 
                WHERE LOWER(username) = LOWER(:u)
                UNION
                SELECT username FROM public.child_profiles 
                WHERE LOWER(username) = LOWER(:u)
                """,
                params={"u": child_username},
                ttl=0
            )
            if not existing.empty:
                st.error("That username is already taken.")
            else:
                try:
                    hashed = hash_password(child_pass)
                    with conn.session as s:
                        s.execute(
                            text("""
                                INSERT INTO public.child_profiles 
                                    (username, parent_username, display_name)
                                VALUES (:u, :p, :d)
                            """),
                            {
                                "u": child_username,
                                "p": parent_username,
                                "d": child_username
                            }
                        )
                        s.execute(
                            text("""
                                INSERT INTO private.user_creds (username, password)
                                VALUES (:u, :p)
                            """),
                            {"u": child_username, "p": hashed}
                        )
                        s.commit()
                    st.success(f"✅ Account created for {child_username}.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error creating account: {e}")
else:
    st.subheader("➕ Create Child Account")
    st.warning(f"You have reached your limit of {max_children} child accounts. Contact us if you need more.")

# ------------------------------------------------
# Section 3 — Change Password
# ------------------------------------------------
# ------------------------------------------------
# Section 3 — Change Password
# ------------------------------------------------
with st.expander("🔒 Change Your Password"):
    with st.form("change_password_form"):
        current_pass = st.text_input("Current Password", type="password")
        new_parent_pass = st.text_input("New Password", type="password")
        confirm_parent_pass = st.text_input("Confirm New Password", type="password")
        change = st.form_submit_button("Update Password")

    if change:
        if not current_pass or not new_parent_pass:
            st.error("All fields are required.")
        elif new_parent_pass != confirm_parent_pass:
            st.error("Passwords do not match.")
        else:
            creds = conn.query(
                "SELECT password FROM private.user_creds WHERE LOWER(username) = LOWER(:u)",
                params={"u": parent_username},
                ttl=0
            )
            from utils.auth_utils import verify_password
            if creds.empty or not verify_password(current_pass, creds.iloc[0]["password"]):
                st.error("Current password is incorrect.")
            else:
                hashed = hash_password(new_parent_pass)
                with conn.session as s:
                    s.execute(
                        text("""
                            UPDATE private.user_creds 
                            SET password = :p 
                            WHERE LOWER(username) = LOWER(:u)
                        """),
                        {"p": hashed, "u": parent_username}
                    )
                    s.commit()
                st.success("✅ Password updated successfully.")

# ------------------------------------------------
# Section 4 — Account Info
# ------------------------------------------------
st.subheader("📧 Account Info")
st.write(f"**Username:** {parent_username}")
st.write(f"**Email:** {email}")