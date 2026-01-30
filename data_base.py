import streamlit as st
import hashlib
from sqlalchemy import create_engine, text

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Initialize connection
conn = st.connection("postgresql", type="sql")

def verify_login(username, password):
    """Checks if the user exists and the password is correct."""
    hashed = hash_password(password)
    # conn.query returns a DataFrame; we check if it has any rows
    result = conn.query(
        "SELECT * FROM users WHERE username = :u AND password = :p",
        params={"u": username, "p": hashed},
        ttl=0 # Don't cache login checks!
    )
    return len(result) > 0

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
