import streamlit as st
import hashlib
from sqlalchemy import create_engine, text
import requests
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Initialize connection
conn = st.connection("postgresql", type="sql")

def verify_login(username, password):
    """Checks if the user exists and the password is correct."""
    hashed = hash_password(password)
    # conn.query returns a DataFrame; we check if it has any rows
    result = conn.query(
        "SELECT is_admin, is_approved FROM users WHERE LOWER(username) = LOWER(:u) AND password = :p",
        params={"u": username, "p": hashed},
        ttl=0 # Don't cache login checks!
    )
    if not result.empty:
        # Return a dictionary of the user's status
        user_dict = result.iloc[0].to_dict()
        #print("--- TERMINAL DEBUG: USER DATA ---")
        #print(user_dict) 
        #print("---------------------")
        return user_dict
    return None

def get_user_progress(username):
    """Fetches all steps completed by this user."""
    result = conn.query(
        "SELECT step FROM progress WHERE id = :u",
        params={"u": username},
        ttl=0
    )
    return result["step"].tolist()

def save_and_unlock(phase_name):
    """Saves a new step for the current user and triggers navigation."""
    user_id = st.session_state.get("user_id", "Guest")
    
    with conn.session as s:
        s.execute(
            text("""
                INSERT INTO progress (id, step) VALUES (:u, :s)
                ON CONFLICT (id, step) DO NOTHING
            """), # <--- Wrapped in text()
            {"u": user_id, "s": phase_name}
        )
        s.commit()
    
    # ... rest of your session_state logic


    if 'unlocked_pages' not in st.session_state:
        st.session_state.unlocked_pages = ["Home"]
    if phase_name not in st.session_state.unlocked_pages:
        st.session_state.unlocked_pages.append(phase_name)

def save_only(step_name):
    """Saves a new step for the current user without switching pages."""
    user_id = st.session_state.get("user_id", "Guest")
    with conn.session as s:
        s.execute(
            text("""
                INSERT INTO progress (id, step) VALUES (:u, :s)
                ON CONFLICT (id, step) DO NOTHING
            """),
            {"u": user_id, "s": step_name}
        )
        s.commit()

import requests
import streamlit as st

def notify_discord_new_request(username):
    webhook_url = st.secrets.get("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        print("Discord Webhook URL not found in secrets.")
        return

    payload = {
        "embeds": [
            {
                "title": "🚀 New User Registration Request",
                "description": f"User **{username}** is waiting for approval.",
                "color": 5814783,  # This is a nice "Discord Blue"
                "fields": [
                    {
                        "name": "Action Required",
                        "value": "Log in to the [Admin Dashboard](https://kidscode.streamlit.app) to approve."
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send Discord notification: {e}")

def log_final_activity():
    """Logs the stay duration for the current page before the session ends."""
    if "start_time" in st.session_state and "current_page" in st.session_state:
        duration = round(time.time() - st.session_state.start_time, 2)
        user = st.session_state.get("user_id", "Anonymous")
        
            

# Only log if they were actually on the page for a moment
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
                print(f"Final log error: {e}")

def notify_discord_feedback(username, category, message):
    webhook_url = st.secrets.get("DISCORD_WEBHOOK_URL")
    if not webhook_url: return

    payload = {
        "embeds": [
            {
                "title": f"💬 New Feedback: {category}",
                "description": f"**From:** {username}\n\n**Message:**\n{message}",
                "color": 3066993,  # A nice Emerald Green
                "footer": {"text": "View details on the Admin Dashboard"}
            }
        ]
    }
    import requests
    requests.post(webhook_url, json=payload)
