import streamlit as st
from sqlalchemy import text

def save_challenge_submission(page_title, content, status='draft'):
    from data_base import conn
    """Saves or updates a user challenge. Status can be 'draft', 'pending', 'approved'."""
    user_id = st.session_state.get("user_id", "Guest")
    
    with conn.session as s:
        s.execute(
            text("""
                INSERT INTO challenge_submissions (user_id, page_title, content, status, last_updated)
                VALUES (:u, :p, :c, :s, CURRENT_TIMESTAMP)
                ON CONFLICT (user_id, page_title) 
                DO UPDATE SET 
                    content = EXCLUDED.content,
                    status = EXCLUDED.status,
                    last_updated = CURRENT_TIMESTAMP
            """),
            {"u": user_id, "p": page_title, "c": content, "s": status}
        )
        s.commit()

def get_challenge_submission(page_title):
    from data_base import conn
    """Fetches the existing draft for a user so they don't lose work."""
    user_id = st.session_state.get("user_id", "Guest")
    result = conn.query(
        "SELECT content, status FROM challenge_submissions WHERE user_id = :u AND page_title = :p",
        params={"u": user_id, "p": page_title},
        ttl=0
    )
    if not result.empty:
        return result.iloc[0].to_dict()
    return {"content": "", "status": "Not Started"}
