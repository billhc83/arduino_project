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
    next_title = None
    if idx + 1 < len(titles_norm):
        next_norm = titles_norm[idx + 1]
        next_title = list(pages_map.keys())[list(pages_map_norm.keys()).index(next_norm)]
        save_and_unlock(next_title)
        if next_title not in unlocked_pages:
            unlocked_pages.append(next_title)
    st.session_state.unlocked_pages = unlocked_pages

    # Optional signal for UI
    st.session_state.just_completed_step = current_page_title

    st.rerun()