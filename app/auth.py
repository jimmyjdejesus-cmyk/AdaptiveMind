from __future__ import annotations

"""Authentication utilities for the FastAPI backend.

Provides JWT-based authentication with simple role-based access control
using OAuth2 password flow. This module is intentionally minimal and
defaults to an in-memory user store for demonstration.
"""

from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional
import os

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# Configuration values can be overridden via environment variables or config files
SECRET_KEY = os.getenv("JARVIS_AUTH_SECRET", "change_me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JARVIS_AUTH_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    """Response model for access tokens."""

    access_token: str
    token_type: str


# Example in-memory user database. Replace with real user management as needed.
fake_users_db: Dict[str, Dict[str, str]] = {
    "admin": {
        "username": "admin",
        "hashed_password": bcrypt.hashpw(b"adminpass", bcrypt.gensalt()).decode("utf-8"),
        "role": "admin",
    },
    "user": {
        "username": "user",
        "hashed_password": bcrypt.hashpw(b"userpass", bcrypt.gensalt()).decode("utf-8"),
        "role": "user",
    },
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""

    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def authenticate_user(username: str, password: str) -> Optional[Dict[str, str]]:
    """Authenticate a user from the in-memory store."""

    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Retrieve the current user from the JWT token."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user


def role_required(required_role: str) -> Callable:
    """Dependency factory that ensures the current user has the given role."""

    async def dependency(current_user: Dict[str, Any] = Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return dependency


async def login_for_access_token(form_data: OAuth2PasswordRequestForm) -> Token:
    """Validate user credentials and return an access token."""

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user["username"], "role": user["role"]})
    return Token(access_token=access_token, token_type="bearer")

