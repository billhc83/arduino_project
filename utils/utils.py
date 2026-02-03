import streamlit as st
import base64
from io import BytesIO
import os


# utils.py

@st.cache_data(ttl=86400)  # Caches for 24 hours (86400 seconds)
def get_user_stats(username):
    from data_base import save_and_unlock, save_only, log_final_activity, conn

    """Calculates total hours spent by a specific user."""
    query = """
        SELECT SUM(stay_duration_seconds) / 3600 as total_hours 
        FROM activity_logs 
        WHERE username = :u
    """
    df = conn.query(query, params={"u": username}, ttl=0)
    
    if not df.empty and df.iloc[0]['total_hours'] is not None:
        return round(df.iloc[0]['total_hours'], 2)
    return 0.0



import re

def get_automated_pages(directory="pages"):
    """
    Dynamically load all .py pages in `directory`.
    - Admin pages are skipped for non-admins
    - Home page is marked as default
    - Returns an **ordered dict** suitable for navigation and step completion
    """
    pages_dict = {}
    is_admin = st.session_state.get("is_admin", False)

    # Gather all page files first
    page_files = [
        f for f in os.listdir(directory)
        if f.endswith(".py") and ("Admin" not in f or is_admin)
    ]

    # Sort numerically if filenames contain numbers, otherwise alphabetically
    def sort_key(filename):
        # extract first number in filename
        m = re.search(r'\d+', filename)
        return int(m.group()) if m else float('inf'), filename.lower()

    page_files.sort(key=sort_key)

    for filename in page_files:
        path = os.path.join(directory, filename)
        is_home = "Home" in filename
        page_obj = st.Page(path, default=is_home)

        # Use the page title as key for simplicity
        pages_dict[page_obj.title] = page_obj

    return pages_dict




def logout_button(in_sidebar=True):
    # Choose where to draw the button
    target = st.sidebar if in_sidebar else st
    
    if target.button("Log Out 🚪", type="secondary", use_container_width=True):
        log_final_activity()
        # 1. Clear session data
        keys_to_clear = ["user_id", "unlocked_pages", "last_user", "next_page", "current_page_title"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        # 2. Redirect back to start
        st.rerun()

def sticky_navbar():

    st.divider()

    st.markdown("""
            <style>
                /* Push the sidebar content down slightly so buttons aren't cramped */
                [data-testid="stSidebarNav"] {
                    padding-top: 20px !important;
                }
                /* Style the logout button specifically */
                div[data-testid="stSidebar"] .stButton > button {
                    border-radius: 20px;
                }
            </style>
        """, unsafe_allow_html=True)

    # 2. Add buttons to the TOP of the sidebar
    with st.sidebar:
        col1, col2 = st.columns(2)
            
        with col1:
            if st.button("🚪Log Out", type="secondary", use_container_width=True, key="nav_logout"):
                st.divider()
                keys_to_clear = ["user_id", "unlocked_pages", "last_user", "next_page"]
                for key in keys_to_clear:
                        if key in st.session_state:
                            del st.session_state[key]
                
                st.rerun()
import os
import streamlit as st
from data_base import save_only, save_and_unlock  # your DB functions
from utils.steps import complete_step_and_continue

def hover_zoom_at_cursor(image, width=800, height=600, zoom_factor=2.5, key="unique"):
    # Convert PIL image to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    container_id = f"zoom-container-{key}"
    
    # CSS & JavaScript for dynamic transform-origin
    html_code = f"""
    <div id="{container_id}" class="zoom-container">
        <img src="data:image/png;base64,{img_str}" id="img-{key}">
    </div>

    <style>
    #{container_id} {{
        width: {width}px;
        height: {height}px;
        overflow: hidden;
        border: 1px solid #ccc;
        position: relative;
    }}
    #{container_id} img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        transition: transform 0.1s ease-out; /* Smooth but responsive */
        transform-origin: center center;
    }}
    #{container_id}:hover img {{
        transform: scale({zoom_factor});
        cursor: crosshair;
    }}
    </style>

    <script>
    (function() {{
        const container = document.getElementById("{container_id}");
        const img = document.getElementById("img-{key}");

        container.addEventListener("mousemove", function(e) {{
            const rect = container.getBoundingClientRect();
            // Calculate mouse position as a percentage of the container size
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            // Move the zoom center to the mouse position
            img.style.transformOrigin = x + "% " + y + "%";
        }});

        // Reset origin when mouse leaves
        container.addEventListener("mouseleave", function() {{
            img.style.transformOrigin = "center center";
        }});
    }})();
    </script>
    """
    
    st.components.v1.html(html_code, height=height+20)

    from sqlalchemy import text

def create_new_user(username, password):
    """Admin utility to manually add a user to the cloud database."""
    hashed = hash_password(password)
    try:
        with conn.session as s:
            s.execute(
                text("INSERT INTO users (username, password) VALUES (:u, :p)"),
                {"u": username, "p": hashed}
            )
            s.commit()
        return True, f"User {username} created successfully!"
    except Exception as e:
        return False, str(e)

