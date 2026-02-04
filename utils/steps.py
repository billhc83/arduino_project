# utils/steps.py
import streamlit as st
from data_base import save_only, save_and_unlock
import os

def complete_step_and_continue(pages_map, current_page_title=None):
    """
    Saves current step, unlocks next page, shows a user-closable message, and reruns Streamlit.
    pages_map: dict of {title: st.Page}
    current_page_title: title of the page calling this function
    """
    import streamlit as st

    # Use session_state if current_page_title not given
    if current_page_title is None:
        current_page_title = st.session_state.get("current_page")
    if not current_page_title:
        st.error("Cannot determine current page for completion.")
        return

    # Normalize titles
    def normalize(s):
        return s.lower().replace(" ", "_").strip()

    pages_map_norm = {normalize(k): v for k, v in pages_map.items()}
    unlocked_pages = st.session_state.get("unlocked_pages", [])

    current_norm = normalize(current_page_title)
    if current_norm not in pages_map_norm:
        st.error(f"Unknown step: {current_page_title}")
        return

    # Save current step
    save_only(current_page_title)

    # Unlock next step
    titles_norm = list(pages_map_norm.keys())
    idx = titles_norm.index(current_norm)
    print(idx)
    next_title = None
    if idx + 1 < len(titles_norm):
        next_norm = titles_norm[idx + 1]
        print(next_norm)
        next_title = list(pages_map.keys())[list(pages_map_norm.keys()).index(next_norm)]
        save_and_unlock(next_title)
        if next_title not in unlocked_pages:
            unlocked_pages.append(next_title)
        # 2. THE SPECIAL CASE: If finishing Project 10, find the first challenge in range
    if current_norm.startswith("project_nine"):
        # Automate the list: Grab everything in the 100-150 range from your map
       all_titles = list(pages_map.keys())
        # 2. Find the first title that is a challenge
       first_challenge = next((t for t in all_titles if "Challenge" in t), None)
       if first_challenge:
            # 4. Save and Unlock using your existing function
            save_and_unlock(first_challenge)
            if first_challenge not in unlocked_pages:
                unlocked_pages.append(first_challenge)
    st.session_state.unlocked_pages = unlocked_pages

    # Optional signal for UI
    st.session_state.just_completed_step = current_page_title

    st.rerun()