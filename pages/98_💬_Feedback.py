import streamlit as st
from data_base import conn

st.title("💬 Project Feedback")
st.write("Have a suggestion or found a bug? Let us know!")

with st.form("feedback_form", clear_on_submit=True):
    category = st.selectbox("Category", ["Bug Report", "Feature Suggestion", "General Comment"])
    message = st.text_area("Your Feedback")
    
    if st.form_submit_button("Submit"):
        if message.strip():
            # ... your existing DB insert code ...
            
            # Trigger the new notification
            from data_base import notify_discord_feedback
            notify_discord_feedback(st.session_state.user_id, category, message)
            
            st.success("Thank you! Your feedback has been logged.")
