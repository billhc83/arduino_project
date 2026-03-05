import resend
import streamlit as st
import secrets
from datetime import datetime, timezone, timedelta
from sqlalchemy import text

resend.api_key = st.secrets["RESEND_API_KEY"]
BASE_URL = st.secrets["BASE_URL"]

def send_verification_email(username: str, email: str):
    """Generate a token, store it, and send the verification email."""
    conn = st.connection("postgresql", type="sql")
    
    # generate a secure token valid for 24 hours
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
    
    # store token in db
    with conn.session as s:
        # clear any existing tokens for this user first
        s.execute(
            text("DELETE FROM private.email_verifications WHERE username = :username"),
            {"username": username}
        )
        s.execute(
            text("""
                INSERT INTO private.email_verifications (username, token, expires_at)
                VALUES (:username, :token, :expires_at)
            """),
            {"username": username, "token": token, "expires_at": expires_at}
        )
        s.commit()
    
    # send the email
    verification_url = f"{BASE_URL}?verify_token={token}"
    
    resend.Emails.send({
        "from": "noreply@kidscode.ca",  # replace with your verified domain
        "to": email,
        "subject": "Verify your account",
        "html": f"""
            <p>Hi {username},</p>
            <p>Click the link below to verify your account:</p>
            <p><a href="{verification_url}">Verify my account</a></p>
            <p>This link expires in 24 hours.</p>
            <p>If you did not sign up, you can ignore this email.</p>
        """
    })