import hashlib
import bcrypt

def is_sha256(hash_string: str) -> bool:
    """Detect if a stored hash is old SHA256 format."""
    return (
        len(hash_string) == 64 and 
        all(c in '0123456789abcdef' for c in hash_string.lower())
    )

def hash_password(password: str) -> str:
    """Hash a new password with bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against either SHA256 or bcrypt hash."""
    if is_sha256(stored_hash):
        # old format - check against SHA256
        return hashlib.sha256(password.encode()).hexdigest() == stored_hash
    else:
        # new format - check against bcrypt
        return bcrypt.checkpw(password.encode(), stored_hash.encode())