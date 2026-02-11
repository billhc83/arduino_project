import streamlit as st
from utils.utils import get_automated_pages, sticky_navbar
from data_base import get_user_progress

# ---------------- 1. Session defaults ----------------
st.session_state.setdefault("user_id", None)
st.session_state.setdefault("is_admin", False)
st.session_state.setdefault("unlocked_pages", [])
st.session_state.setdefault("current_page", None)

# ---------------- 2. Load all pages ----------------
pages_map = get_automated_pages("pages")
st.session_state.pages_map = pages_map

# ---------------- 3. Load user progress ----------------
user_steps = []
if st.session_state.user_id:
    db_steps = get_user_progress(st.session_state.user_id)
    # convert to step IDs (filenames without .py)
    user_steps = [s.replace(" ", "_") for s in db_steps]  # match pages_map keys

# ---------------- 4. Determine unlocked pages ----------------
if st.session_state.user_id:
    unlocked_pages = ["Home", "Getting_Started"] + user_steps
    if "Feedback" not in unlocked_pages:
        unlocked_pages.append("Feedback")
    if st.session_state.is_admin in [True, "true", "True"]:
        if "Admin" not in unlocked_pages:
            unlocked_pages.append("Admin")
else:
    unlocked_pages = ["Login", "Register"]

st.session_state.unlocked_pages = unlocked_pages

# Load pages
pages_map = get_automated_pages("pages")
st.session_state.pages_map = pages_map

# Normalize
def normalize(s):
    return s.lower().replace(" ", "_").strip()

pages_map_norm = {normalize(k): v for k, v in pages_map.items()}
unlocked_pages_norm = [normalize(p) for p in st.session_state.get("unlocked_pages", [])]

# Build allowed_pages safely
allowed_pages = [v for k, v in pages_map_norm.items() if k in unlocked_pages_norm]

#st.write("Allowed pages:", [p.title for p in allowed_pages])  # debug


# Optional debug (can remove later)
#st.write("Allowed pages:", [p.title for p in allowed_pages])


# ---------------- 6. Ensure current page is valid ----------------
if st.session_state.get("current_page") not in pages_map:
    if st.session_state.user_id and "Home" in pages_map:
        st.session_state.current_page = "Home"
    else:
        st.session_state.current_page = list(pages_map.keys())[0]
if st.session_state.user_id:
    sticky_navbar()
    
st.session_state.pages_map = pages_map
# ---------------- 7. Navigation widget ----------------
if not allowed_pages:
    st.error("No pages available! Check your pages folder and unlocked_pages.")
else:
    pg = st.navigation(allowed_pages)
    if pg:
        from data_base import log_final_activity
        import time
        log_final_activity()
        st.session_state.current_page = pg.title
        st.session_state.start_time = time.time()
        pg.run()

# ---------------- 8. Sticky navbar ----------------
