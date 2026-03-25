# This file contains all security logic
# Password hashing and JWT token creation/verification

from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt

# --- CONFIGURATION ---
SECRET_KEY = "reflecta-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- PASSWORD HASHING ---
# Using bcrypt directly instead of passlib to avoid version conflicts
def hash_password(password: str) -> str:
    # encode() converts string to bytes because bcrypt works with bytes
    # gensalt() generates a random salt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # checkpw re-hashes the plain password and compares to stored hash
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

# --- JWT TOKENS ---
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None