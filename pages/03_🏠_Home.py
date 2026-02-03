import streamlit as st
from utils.utils import get_automated_pages, get_user_stats
from data_base import get_user_progress

# 1. Get User Info
user = st.session_state.get("user_id", "Guest")

st.title(f"👋 Welcome back, {user}!")

user = st.session_state.get("user_id")

if user:
    total_time = get_user_stats(user)
    
    st.subheader(f"Welcome back, {user}!")
    
    # Display the stat in a nice card format
    st.title(f"{total_time} Hours Of Learning Completed")


# 1. Get total projects from files
all_pages = get_automated_pages("pages")
project_titles = [title for title in all_pages.keys() if "Project" in title]
total_projects = len(project_titles)

# 2. Get user progress (ONLY items in the database)
user = st.session_state.get("user_id", "Guest")
db_steps = get_user_progress(user) # This calls your SELECT step FROM progress

# 3. FIX: Only count if the database string is "Completed Project One" 
# or matches your save_only format exactly.
# If your utils.py saves as "Completed Project One", use that here:
completed_count = 0
for step in db_steps:
    if "Completed" in step and any(proj in step for proj in project_titles):
        completed_count += 1

# 4. Progress Bar
if total_projects > 0:
    # Ensure ratio is 0.0 to 1.0
    ratio = min(float(completed_count / total_projects), 1.0)
    
    st.subheader(f"You have completed {completed_count} out of {total_projects} projects")
    st.progress(ratio)
    st.write(f"**{int(ratio * 100)}%** course complete!")



st.divider()

# 5. Quick Links to Unlocked Projects
st.markdown("### 📚 Your Lessons")
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

