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

# 6. Build the initial allowed list
allowed_pages = [p for p in pages_map.values() if p.title in st.session_state.unlocked_pages]

# 2. KEEP THIS: Ensure Home is at the absolute top (Index 0)
if "Home" in pages_map:
    home_page = pages_map["Home"]
    # If Home is already in the list, move it to index 0
    if home_page in allowed_pages:
        allowed_pages.remove(home_page)
    allowed_pages.insert(0, home_page)

# 3. ADD THIS: Inject Feedback at the bottom of the visible list
if "Feedback" in pages_map:
    f_page = pages_map["Feedback"]
    if f_page not in allowed_pages:
        allowed_pages.append(f_page) 

if st.session_state.get("is_admin") in [True, "true", "True"]:
    if "Admin" in pages_map:
        a_page = pages_map["Admin"]
        if a_page not in allowed_pages:
            allowed_pages.append(a_page)

# 3. FORCE ADMIN INJECTION
user_is_admin = st.session_state.get("is_admin") in [True, "true", "True"]

if user_is_admin:
    if "Admin" in pages_map:
        admin_page_obj = pages_map["Admin"]
        if admin_page_obj not in allowed_pages:
            allowed_pages.append(admin_page_obj)
            print("✅ SUCCESS: Admin object added to allowed_pages list")
    else:
        print("❌ ERROR: Key 'Admin' not found in pages_map")
else:
    print(f"🚫 BLOCKED: is_admin is {st.session_state.get('is_admin')}")

print("--- ALL DETECTED PAGE TITLES ---")
for title, page_obj in pages_map.items():
    # .title is the visible name, and we'll print the object to see the path
    print(f"Key in Map: '{title}' | Page Title: '{page_obj.title}'")
print("---------------------------------")
# 7. Define Navigation
pg = st.navigation(allowed_pages)

import time
# 1. Check for a heartbeat (every 5 minutes)
HEARTBEAT_INTERVAL = 300 # 5 minutes
last_heartbeat = st.session_state.get("last_heartbeat", st.session_state.start_time)

if (time.time() - last_heartbeat) > HEARTBEAT_INTERVAL:
    # Update the current page's time without waiting for a switch
    duration = round(time.time() - st.session_state.start_time, 2)
    # Use an 'UPSERT' or just a fresh log entry
    # (Writing the code here to insert a heartbeat log)
    st.session_state.last_heartbeat = time.time()

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

import time

# 1. Initialize tracking variables
if "current_page" not in st.session_state:
    st.session_state.current_page = "None"
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# 2. Detect Page Change
# 'pg' is the result of st.navigation(allowed_pages)
new_page_title = pg.title 

if new_page_title != st.session_state.current_page:
    # They just moved! Calculate stay time for the PREVIOUS page
    if st.session_state.current_page != "None":
        duration = round(time.time() - st.session_state.start_time, 2)
        user = st.session_state.get("user_id", "Anonymous")
        
        # Only log if they stayed for more than 2 seconds (ignores accidental clicks)
        if duration > 2:
            try:
                from sqlalchemy import text
                with conn.session as s:
                    s.execute(
                        text("INSERT INTO activity_logs (username, page_name, stay_duration_seconds) VALUES (:u, :p, :d)"),
                        {"u": user, "p": st.session_state.current_page, "d": duration}
                    )
                    s.commit()
            except Exception as e:
                print(f"Logging error: {e}")

    # Reset for the new page
    st.session_state.current_page = new_page_title
    st.session_state.start_time = time.time()
    
# 10. Run the page
pg.run()

