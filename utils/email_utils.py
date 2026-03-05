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


def send_temp_password(email: str) -> bool:
    import secrets
    import string
    """Generate a temp password, update db, send via email. Returns True if email found."""
    conn = st.connection("postgresql", type="sql")

    # find user by email
    result = conn.query(
        "SELECT username FROM public.users WHERE LOWER(email) = LOWER(:e)",
        params={"e": email},
        ttl=0
    )

    if result.empty:
        return False

    username = result.iloc[0]["username"]

    # generate a readable temp password
    alphabet = string.ascii_letters + string.digits
    temp_password = ''.join(secrets.choice(alphabet) for _ in range(10))

    # hash and update in db
    from utils.auth_utils import hash_password
    hashed = hash_password(temp_password)

    with conn.session as s:
        s.execute(
            text("""
                UPDATE private.user_creds 
                SET password = :p 
                WHERE LOWER(username) = LOWER(:u)
            """),
            {"p": hashed, "u": username}
        )
        s.commit()

    # send email
    resend.Emails.send({
        "from": "noreply@kidscode.ca",
        "to": email,
        "subject": "Your temporary password",
        "html": f"""
            <p>Hi {username},</p>
            <p>Your temporary password is:</p>
            <h2>{temp_password}</h2>
            <p>Please log in and change your password as soon as possible.</p>
            <p>If you did not request this, please contact us immediately.</p>
        """
    })

    return True