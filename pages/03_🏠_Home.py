import streamlit as st
from utils.utils import get_automated_pages, get_user_stats

# -----------------------------
# 1️⃣ Helpers
# -----------------------------
def normalize(s: str) -> str:
    """Normalize string for consistent comparison."""
    return s.lower().replace(" ", "_").replace("-", "_").strip()

def is_project_page(title: str) -> bool:
    """Return True if the page is a project page."""
    title_norm = title.lower().replace("_", " ").replace("-", " ")
    return "project" in title_norm


# -----------------------------
# 2️⃣ User info
# -----------------------------
user = st.session_state.get("user_id", "Guest")
st.title(f"👋 Welcome back, {user}!")

if user != "Guest":
    total_time = get_user_stats(user)
    st.subheader(f"{total_time} Hours Of Learning Completed")

st.divider()

# -----------------------------
# 3️⃣ Load all pages
# -----------------------------
all_pages = get_automated_pages("pages")  # dict {title: page_object}

# Only project pages
project_pages = {title: page for title, page in all_pages.items() if is_project_page(title)}
total_projects = len(project_pages)

# Normalize mapping
project_norm_map = {normalize(title): title for title in project_pages.keys()}

# Debug: see what pages are loaded
#st.write("All pages discovered:", all_pages)
#st.write("Filtered project pages:", project_pages)

# -----------------------------
# 4️⃣ User progress from unlocked pages
# -----------------------------
unlocked_pages = st.session_state.get("unlocked_pages", [])
unlocked_norm = {normalize(p) for p in unlocked_pages}

# Count completed projects by intersection with project pages
completed_count = len(set(project_norm_map.keys()) & unlocked_norm)

# -----------------------------
# 5️⃣ Progress bar
# -----------------------------
if total_projects > 0:
    ratio = min(float(completed_count / total_projects), 1.0)
    st.subheader(f"You have completed {completed_count} out of {total_projects} projects")
    st.progress(ratio)
    st.write(f"**{int(ratio * 100)}%** course complete!")

st.divider()

# -----------------------------
# 6️⃣ Show unlocked / locked project cards
# -----------------------------
st.markdown("### 📚 Your Projects")

projects_per_row = 5
project_items = list(project_pages.items())

TITLE_HEIGHT_PX = 48  # adjust if titles wrap more

for i in range(0, len(project_items), projects_per_row):
    cols = st.columns(projects_per_row)

    for col, (title, page) in zip(cols, project_items[i:i + projects_per_row]):
        with col:
            with st.container(border=True):

                # Fixed-height title area
                st.markdown(
                    f"""
                    <div style="
                        height:{TITLE_HEIGHT_PX}px;
                        text-align:center;
                        font-weight:600;
                        line-height:1.2;
                        overflow:hidden;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                    ">
                        {title}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Button area (natural height)
                key_safe_title = normalize(title)

                if key_safe_title in unlocked_norm:
                    if st.button(
                        "✅ Open",
                        use_container_width=True,
                        key=f"open_{key_safe_title}"
                    ):
                        st.switch_page(page)
                else:
                    st.button(
                        "🔒 Locked",
                        disabled=True,
                        use_container_width=True,
                        key=f"locked_{key_safe_title}"
                    )



from utils.badges import badges  # <- import the import streamlit as st

# ... your dictionary and session state setup ...
import streamlit as st

# ... your badge dictionary ...

import streamlit as st

# Define the order of tiers you want to display
import streamlit as st

# Define fun, child-friendly names for your tiers
TIER_THEMES = {
    "orange": {"label": "🌌 Galactic Legend", "color": "violet", "emoji": "👑"},
    "blue": {"label": "🌊 Heroic Explorer", "color": "blue", "emoji": "🛡️"},
    "green": {"label": "🌱 Rising Star", "color": "green", "emoji": "⭐"}
}

# The order you want them to appear on the page
TIER_ORDER = ["orange", "blue", "green"]

st.title("🚀 Your Adventure Log")

# 1. Filter unlocked badges
unlocked_badges = [b for b in badges.values() if b["trigger"](unlocked_pages)]

# 2. Iterate through your themed tiers
for tier_key in TIER_ORDER:
    theme = TIER_THEMES[tier_key]
    # Filter badges for this specific tier
    tier_badges = [b for b in unlocked_badges if b.get("tier") == tier_key]
    
    if tier_badges:
        # Fun Header for the Tier
        st.markdown(f"## :{theme['color']}[{theme['label']}]")
        
        # 3. Create the 3-column grid for this tier
        for i in range(0, len(tier_badges), 3):
            cols = st.columns(3)
            chunk = tier_badges[i:i+3]
            
            for idx, badge in enumerate(chunk):
                with cols[idx]:
                    with st.container(border=True):
                        # Combine Badge Icon + Title in the tier's color
                        st.markdown(f"### {badge['icon']}\n**:{theme['color']}[{badge['title']}]**")
                        
                        st.caption(f"{theme['emoji']} {badge['subtitle']}")
                        
                        # Compact points for kids to read easily
                        for point in badge["points"]:
                            st.markdown(f"✨ <small>{point}</small>", unsafe_allow_html=True)
        st.divider()
