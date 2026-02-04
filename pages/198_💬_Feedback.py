import streamlit as st
from data_base import conn
from sqlalchemy import text
import time
st.title("💬 Project Feedback")
st.write("Have a suggestion or found a bug? Let us know!")

with st.form("feedback_form", clear_on_submit=True):
    category = st.selectbox("Category", ["Bug Report", "Feature Suggestion", "General Comment"])
    message = st.text_area("Your Feedback")
    from datetime import datetime
    
    if st.form_submit_button("Submit"):
        if message.strip():
            try:
                with conn.session as s:
                    s.execute(
                        text("""
                            INSERT INTO feedback (username, category, message, created_at)
                            VALUES (:u, :c, :m, :t)
                        """),
                        {
                            "u": st.session_state.user_id,
                            "c": category,
                            "m": message,
                            "t": datetime.utcnow()
                        }
                    )
                    s.commit()
                st.success("Feedback submitted — thank you!")
            except Exception as e:
                st.error(f"Error sending feedback: {e}")
            # Trigger the new notification
            from data_base import notify_discord_feedback
            notify_discord_feedback(st.session_state.user_id, category, message)
            
            st.success("Thank you! Your feedback has been logged.")
