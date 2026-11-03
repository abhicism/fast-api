
import os
import jwt

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


# =====================================
# 1. ENVIRONMENT VARIABLES
# =====================================

# Load variables from .env
load_dotenv()

# Get secret key
SECRET_KEY = os.getenv("SECRET_KEY")

# JWT algorithm
ALGORITHM = "HS256"

# Check secret key
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing from .env")


# =====================================
# 2. PASSWORD HASHING
# =====================================

password_hash = PasswordHash.recommended()


# Hash password
def hash_password(password: str) -> str:
    return password_hash.hash(password)


# Verify password
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password
    )


# =====================================
# 3. CREATE JWT ACCESS TOKEN
# =====================================

def create_access_token(user_id: int) -> str:

    # Token expires after 30 minutes
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)

    # Token payload
    payload = {
        "sub": str(user_id),
        "exp": expires
    }

    # Generate JWT token
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# =====================================
# 4. VERIFY JWT ACCESS TOKEN
# =====================================

def verify_access_token(token: str):

    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Extract user ID
        user_id = payload.get("sub")

        if user_id is None:
            return None

        return int(user_id)

    except (jwt.InvalidTokenError, ValueError):
        return None


# =====================================
# 5. OAUTH2 PASSWORD BEARER
# =====================================

# Tells FastAPI where users obtain their token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


# =====================================
# 6. GET CURRENT AUTHENTICATED USER
# =====================================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    # Verify incoming JWT token
    user_id = verify_access_token(token)

    # Reject invalid or expired tokens
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Return authenticated user's ID
    return user_id
