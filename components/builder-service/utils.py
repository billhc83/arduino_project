import streamlit as st
import re
import os
import base64
from io import BytesIO
from collections import defaultdict

# ─── Constants ───────────────────────────────────────────────────────────────
UTILITY_KEYWORDS = ["Login", "Register", "Home",
                    "Feedback", "Admin", "Parent_Dashboard"]
UTILITY_ORDER    = ["Login", "Register", "Home",
                    "Feedback", "Admin", "Parent_Dashboard"]

# ─── Helpers ─────────────────────────────────────────────────────────────────
def normalize(s):
    if not s or not isinstance(s, str):
        return ""
    return s.lower().replace(" ", "_").strip()

def sort_key(filename):
    numbers = re.findall(r'\d+', filename)
    if len(numbers) >= 2:    return (int(numbers[0]), int(numbers[1]))
    elif len(numbers) == 1:  return (int(numbers[0]), 0)
    return (999, 0)

def derive_title(filename):
    name = filename.replace('.py', '')
    name = re.sub(r'^(\d+_)+', '', name)
    name = name.encode('ascii', 'ignore').decode()
    name = name.replace('_', ' ').strip()
    return name

def section_title(filenames):
    """Derive clean section header — strips trailing Part/Step/etc"""
    title = derive_title(filenames[0])
    title = re.sub(r'\s+(Part|Step|Section|Chapter|Lesson)\s*\d*$', '',
                   title, flags=re.IGNORECASE).strip()
    return title

def valid_page_file(filename):
    """Only process properly named page files — must start with a number"""
    return filename.endswith(".py") and bool(re.match(r'^\d+_', filename))

# ─── Flat Page Map ────────────────────────────────────────────────────────────
def get_automated_pages(directory="pages", default_page="Login"):
    """
    Returns flat {title: page_obj} dict.
    Used for unlock filtering and routing.
    """
    is_admin  = st.session_state.get("is_admin",  False)
    is_parent = st.session_state.get("is_parent", False)

    page_files = [
        f for f in os.listdir(directory)
        if valid_page_file(f)
        and ("Admin"            not in f or is_admin)
        and ("Parent_Dashboard" not in f or is_parent)
    ]
    page_files.sort(key=sort_key)

    pages_map   = {}
    default_set = False

    for filename in page_files:
        path  = os.path.join(directory, filename)
        title = derive_title(filename)

        is_default = (default_page in filename) and not default_set
        if is_default:
            default_set = True

        pages_map[title] = st.Page(path, title=title, default=is_default)

    return pages_map

# ─── Logout Button ────────────────────────────────────────────────────────────
def logout_button(in_sidebar=True):
    from data_base import log_final_activity
    target = st.sidebar if in_sidebar else st
    if target.button("Log Out 🚪", type="secondary",
                     use_container_width=True, key="logout_btn"):
        log_final_activity()
        keys_to_clear = ["user_id", "unlocked_pages", "last_user",
                         "next_page", "current_page_title", "current_page",
                         "is_admin", "is_parent"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# ─── Custom Sidebar Nav ───────────────────────────────────────────────────────
def build_custom_sidebar(pages_map, unlocked_norm, directory="pages"):
    """
    Renders custom sidebar navigation:
      1. Utility links at top (Login/Register when logged out,
         Home/Feedback/Admin when logged in)
      2. Projects reversed — newest at top
         - Single page  → plain button
         - Multi step   → expander, auto-open if current project
      3. Challenges section at bottom
      4. Logout button at bottom (logged in only)
    """
    is_admin  = st.session_state.get("is_admin",  False)
    is_parent = st.session_state.get("is_parent", False)
    current   = st.session_state.get("current_page") or ""

    # ── Get valid page files only ─────────────────────────────────────────────
    page_files = [
        f for f in os.listdir(directory)
        if valid_page_file(f)
        and ("Admin"            not in f or is_admin)
        and ("Parent_Dashboard" not in f or is_parent)
    ]

    # ── Count steps per project number ───────────────────────────────────────
    project_groups = defaultdict(list)
    for f in page_files:
        if any(kw in f for kw in UTILITY_KEYWORDS): continue
        if "Challenge" in f: continue
        nums = re.findall(r'\d+', f)
        if nums:
            project_groups[nums[0]].append(f)

    # ── Separate into buckets ─────────────────────────────────────────────────
    utility_files   = []
    project_files   = []
    challenge_files = []

    for f in page_files:
        if any(kw in f for kw in UTILITY_KEYWORDS):
            utility_files.append(f)
        elif "Challenge" in f:
            challenge_files.append(f)
        else:
            project_files.append(f)

    utility_files.sort(key=lambda f: next(
        (i for i, kw in enumerate(UTILITY_ORDER) if kw in f), 99
    ))
    project_files.sort(key=sort_key, reverse=True)
    challenge_files.sort(key=sort_key)

    # ── Nav button ────────────────────────────────────────────────────────────
    btn_counter = [0]

    def nav_button(title):
        if title not in pages_map:
            return
        is_current = normalize(title) == normalize(current)
        st.page_link(
            pages_map[title],
            label=f"**{title}**" if is_current else title,
            use_container_width=True,
            icon="▶" if is_current else None
        )

    # ── Render sidebar ────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
<style>
/* Tighten link spacing */
[data-testid="stSidebar"] [data-testid="stPageLink"] {
    padding: 2px 0;
    margin: 0;
}
/* Active page highlight */
[data-testid="stSidebar"] [data-testid="stPageLink-active"] a {
    background-color: rgba(255, 75, 75, 0.2);
    border-radius: 8px;
    font-weight: 600;
}
/* Hover state */
[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)
        # 1. Utilities
        for filename in utility_files:
            title = derive_title(filename)
            if normalize(title) not in unlocked_norm:
                continue
            nav_button(title)

        # 2. Projects (only when logged in)
        if st.session_state.get("user_id") is not None:
            st.divider()
            seen = set()
            for filename in project_files:
                title       = derive_title(filename)
                nums        = re.findall(r'\d+', filename)
                project_num = nums[0] if nums else "999"

                if normalize(title) not in unlocked_norm:
                    continue
                if project_num in seen:
                    continue

                is_multi = len(project_groups.get(project_num, [])) > 1

                if is_multi:
                    step_titles = [derive_title(f) for f in project_groups[project_num]]
                    is_active   = any(normalize(t) == normalize(current)
                                    for t in step_titles)
                    with st.expander(section_title(project_groups[project_num]),
                                    expanded=is_active):
                        # Sort steps ascending within the expander
                        sorted_steps = sorted(project_groups[project_num], key=sort_key)
                        for step_file in sorted_steps:
                            step_title = derive_title(step_file)
                            if normalize(step_title) in unlocked_norm:
                                nav_button(step_title)
                    seen.add(project_num)
                else:
            # ADD THIS: Handle single-file projects
                    if normalize(title) in unlocked_norm:
                        nav_button(title)
                        seen.add(project_num)

            # 3. Challenges
            unlocked_challenges = [
                f for f in challenge_files
                if normalize(derive_title(f)) in unlocked_norm
            ]
            if unlocked_challenges:
                st.divider()
                st.caption("Challenges")
                for filename in unlocked_challenges:
                    nav_button(derive_title(filename))

            # 4. Logout
            st.divider()
            logout_button(in_sidebar=True)

# ─── User Stats ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=86400)
def get_user_stats(username):
    from data_base import conn
    query = """
        SELECT SUM(stay_duration_seconds) / 3600 as total_hours 
        FROM activity_logs 
        WHERE username = :u
    """
    df = conn.query(query, params={"u": username}, ttl=0)
    if not df.empty and df.iloc[0]['total_hours'] is not None:
        return round(df.iloc[0]['total_hours'], 2)
    return 0.0

# ─── Hover Zoom ───────────────────────────────────────────────────────────────
def hover_zoom_html(image, height=600, zoom_factor=2.5, key="unique"):
    from PIL import Image
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str      = base64.b64encode(buffered.getvalue()).decode()
    container_id = f"zoom-container-{key}"
    return f"""
    <div id="{container_id}" class="zoom-container">
        <img src="data:image/png;base64,{img_str}" id="img-{key}">
    </div>
    <style>
    #{container_id} {{
        width: 100%;
        height: {height}px;
        overflow: hidden;
        border: 1px solid #ccc;
        position: relative;
    }}
    #{container_id} img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        transition: transform 0.1s ease-out;
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
        const img       = document.getElementById("img-{key}");
        container.addEventListener("mousemove", function(e) {{
            const rect = container.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width)  * 100;
            const y = ((e.clientY - rect.top)  / rect.height) * 100;
            img.style.transformOrigin = x + "% " + y + "%";
        }});
        container.addEventListener("mouseleave", function() {{
            img.style.transformOrigin = "center center";
        }});
    }})();
    </script>
    """

def hover_zoom_at_cursor(image, height=600, zoom_factor=2.5, key="unique"):
    import streamlit.components.v1 as components
    components.html(hover_zoom_html(image, height, zoom_factor, key),
                    height=height + 20)

# ─── Intro Video Player ───────────────────────────────────────────────────────
def intro_player(intro_vid):
    import streamlit.components.v1 as components
    components.html(f"""
        <div style="width:100%;border-radius:16px;overflow:hidden;background:transparent;">
            <video autoplay muted
                style="width:100%;display:block;border-radius:16px;">
                <source src="{intro_vid}" type="video/mp4">
            </video>
        </div>
    """, height=450)

# ─── Create New User ──────────────────────────────────────────────────────────
def create_new_user(username, password):
    from data_base import conn, hash_password
    from sqlalchemy import text
    hashed = hash_password(password)
    try:
        with conn.session as s:
            s.execute(
                text("INSERT INTO public.users (username, is_admin, is_approved) "
                     "VALUES (:u, :a, :ap)"),
                {"u": username, "a": False, "ap": False}
            )
            s.execute(
                text("INSERT INTO private.user_creds (username, password) "
                     "VALUES (:u, :p)"),
                {"u": username, "p": hashed}
            )
            s.commit()
        return True, f"User {username} created successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"
from utils.steps import complete_step_and_continue