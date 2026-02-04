import streamlit as st
from data_base import notify_discord_feedback
from utils.challenge_save_data import save_challenge_submission, get_challenge_submission
# At the top of the page, load their work
existing_data = get_challenge_submission(st.session_state.current_page)

st.title(st.session_state.current_page)
st.write(f"Current Status: **{existing_data['status'].upper()}**")

# The auto-saving text area
st.text_area(
    "Enter your task results:",
    value=existing_data['content'],
    key="challenge_draft_input",
    height=300,
    on_change=lambda: save_challenge_submission(
        st.session_state.current_page, 
        st.session_state.challenge_draft_input, 
        status='draft'
    )
)

if st.button("Final Submit for Review", type="primary"):
    save_challenge_submission(
        st.session_state.current_page, 
        st.session_state.challenge_draft_input, 
        status='pending'
    )
    notify_discord_feedback(
        username=st.session_state.user_id, 
        category="Challenge Submission", 
        message= st.session_state.challenge_draft_input)
    st.success("Work submitted! Admin will unlock the next challenge after review.")
