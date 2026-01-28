import streamlit as st
import sqlite3
import os
import hashlib

# --- DATABASE LOGIC ---

def hash_password(password):
    """Scrambles password so it isn't stored as plain text."""
    return hashlib.sha256(str.encode(password)).hexdigest()

@st.cache_resource
def get_db_connection():
    """Persistent connection with Users and Progress tables."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'progress.db')
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute('PRAGMA journal_mode=WAL;')
    
    # Table for User Login
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, 
            password TEXT
        )
    ''')
    
    # Table for Progress
    conn.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id TEXT, 
            step TEXT,
            PRIMARY KEY (id, step)
        )
    ''')
    conn.commit()
    return conn

def verify_login(username, password):
    """Checks if the user exists and the password is correct."""
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
    return cursor.fetchone() is not None

def get_user_progress(username):
    """Fetches all steps completed by this user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT step FROM progress WHERE id = ?", (username,))
    return [row[0] for row in cursor.fetchall()]

# --- ADDED BACK: Missing functions for course navigation ---

def save_and_unlock(phase_name):
    """Saves a new step for the current user and triggers navigation."""
    user_id = st.session_state.get("user_id", "Guest")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO progress (id, step) VALUES (?, ?)", (user_id, phase_name))
    conn.commit()

    if 'unlocked_pages' not in st.session_state:
        st.session_state.unlocked_pages = ["Home"]
    if phase_name not in st.session_state.unlocked_pages:
        st.session_state.unlocked_pages.append(phase_name)
    

def save_only(step_name):
    """Saves a new step for the current user without switching pages."""
    user_id = st.session_state.get("user_id", "Guest")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO progress (id, step) VALUES (?, ?)", (user_id, step_name))
    conn.commit()
