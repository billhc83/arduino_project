# --- main.py ---
import streamlit as st 
from data_base import verify_login, get_user_progress, save_and_unlock,save_only
from utils import get_automated_pages 
from data_base import conn, hash_password, verify_login, get_user_progress, save_and_unlock, save_only


if "user_id" in st.session_state and st.session_state.user_id:
    if "unlocked_pages" not in st.session_state:
        try:
            user_steps = get_user_progress(st.session_state.user_id)
            # Ensure "Home" and "Information" are always there
            st.session_state.unlocked_pages = list(set(["Home", "Information"] + user_steps))
        except Exception as e:
            st.error(f"Error loading progress: {e}")
#st.write("Available secrets sections:", list(st.secrets.keys()))

# 1. Initialize session state IMMEDIATELY
if "unlocked_pages" not in st.session_state:
    st.session_state.unlocked_pages = ["Home", "Register"]

# 2. Load pages
pages_map = get_automated_pages("pages")
current_user = st.session_state.get("user_id")

# 3. User Change Logic
if "last_user" not in st.session_state or st.session_state.last_user != current_user:
    # If a user just logged in, clear previous progress so it forces a fresh fetch
    if "unlocked_pages" in st.session_state:
        del st.session_state["unlocked_pages"]
        
    if current_user:    
        st.session_state.next_page = "Home" 
    else:
        st.session_state.unlocked_pages = ["Register","Login"]
        st.session_state.next_page = "Login"
    
    st.session_state.last_user = current_user
    st.rerun()

# 4. Database Progress (Same as before)
#db_steps = []
#if current_user:
 #   try:
  #      cursor.execute("SELECT step FROM progress WHERE id=?", (current_user,))
   #     db_steps = [row[0] for row in cursor.fetchall()]
    #except Exception as e:
     #   db_steps = []

# 5. Build unlocked list (Match by title)
# main.py - Step 5
#for step in db_steps:
    # If the step is "Completed Project One", extract "Project One" to unlock it
 #   clean_step = step.replace("Completed ", "") 
    
  #  if clean_step in pages_map and clean_step not in st.session_state.unlocked_pages:
   #     st.session_state.unlocked_pages.append(clean_step)



# 6. Build the initial allowed list
allowed_pages = [p for p in pages_map.values() if p.title in st.session_state.unlocked_pages]

# --- THE SECOND SECTION GOES HERE ---
if "Home" in pages_map:
    home_page = pages_map["Home"]
    if home_page in allowed_pages:
        allowed_pages.remove(home_page)
        allowed_pages.insert(0, home_page)

# 7. Define Navigation
pg = st.navigation(allowed_pages)

# 8. Track current title
if pg:
    st.session_state.current_page_title = pg.title

# 9. CRITICAL: Handle Switch Trigger
if st.session_state.get("next_page"):
    target = st.session_state.next_page
    st.session_state.next_page = None # Clear immediately
    
    if target in pages_map and pages_map[target] in allowed_pages:
        # Stop everything and jump to the target
        st.switch_page(pages_map[target])

if st.session_state.get("user_id"):
    from utils import sticky_navbar
    sticky_navbar()
    
# 10. Run the page
pg.run()

