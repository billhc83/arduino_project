import streamlit as st
from utils.utils import get_automated_pages, build_custom_sidebar, normalize, logout_button
from data_base import get_user_progress, log_final_activity, conn, text
import time

# ── 1. Session defaults ───────────────────────────────────────────────────────
st.session_state.setdefault("user_id",      None)
st.session_state.setdefault("is_admin",     False)
st.session_state.setdefault("is_parent",    False)
st.session_state.setdefault("current_page", None)

if st.session_state.pop("verify_success", False):
    st.success("✅ Email verified! You can now log in.")

# ── 2. Email verification handler ────────────────────────────────────────────
params = st.query_params
if "verify_token" in params:
    token = params["verify_token"]
    result = conn.query(
        """
        SELECT username, expires_at 
        FROM private.email_verifications 
        WHERE token = :token
        """,
        params={"token": token},
        ttl=0
    )
    if result.empty:
        st.error("❌ Invalid or expired verification link.")
    else:
        from datetime import datetime, timezone
        expires_at = result.iloc[0]["expires_at"]
        if datetime.now(timezone.utc) > expires_at:
            st.error("❌ This verification link has expired. Please register again.")
        else:
            username = result.iloc[0]["username"]
            with conn.session as s:
                s.execute(
                    text("""
                        UPDATE public.users 
                        SET email_verified = TRUE, is_approved = TRUE
                        WHERE LOWER(username) = LOWER(:username)
                    """),
                    {"username": username}
                )
                s.execute(
                    text("""
                        DELETE FROM private.email_verifications 
                        WHERE token = :token
                    """),
                    {"token": token}
                )
                s.commit()
            st.session_state.verify_success = True
            st.query_params.clear()

# ── 3. Build flat page map ────────────────────────────────────────────────────
is_logged_in = st.session_state.get("user_id") is not None
default_page = "Home" if is_logged_in else "Login"
pages_map    = get_automated_pages("pages", default_page=default_page)
st.session_state.pages_map = pages_map

# ── 4. Load user progress ─────────────────────────────────────────────────────
user_steps = []
if is_logged_in:
    db_steps   = get_user_progress(st.session_state.user_id)
    user_steps = [s.replace(" ", "_") for s in db_steps]

# ── 5. Determine unlocked pages ───────────────────────────────────────────────
if is_logged_in:
    if st.session_state.get("is_parent", False):
        unlocked_pages = ["Parent_Dashboard"]
    else:
        unlocked_pages = ["Home", "Getting_Started"] + user_steps
        if "Feedback" not in unlocked_pages:
            unlocked_pages.append("Feedback")
        if st.session_state.is_admin in [True, "true", "True"]:
            if "Admin" not in unlocked_pages:
                unlocked_pages.append("Admin")
else:
    unlocked_pages = ["Login", "Register"]

st.session_state.unlocked_pages = unlocked_pages
unlocked_norm = set(normalize(p) for p in unlocked_pages)

# ── 6. Navigation — hidden, only unlocked pages ───────────────────────────────
unlocked_page_objs = [v for k, v in pages_map.items() if normalize(k) in unlocked_norm]
pg = st.navigation(unlocked_page_objs, position="hidden")
if pg:
    log_final_activity()
    st.session_state.current_page = pg.title
    st.session_state.start_time   = time.time()
    pg.run()
# ── 7. Custom sidebar ─────────────────────────────────────────────────────────
build_custom_sidebar(pages_map, unlocked_norm)

# ── 8. Run current page ───────────────────────────────────────────────────────
