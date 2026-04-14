import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
from utils.database import supabase

load_dotenv()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

class CurrentUser:
    def __init__(self, id: str, email: str):
        self.id = id
        self.email = email

def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    """
    Decodes and validates a Supabase Auth JWT or custom JWT to authenticate the user.
    If the JWT is from Supabase, it verifies it using the Supabase API client.
    As a fallback, it checks standard HS256 signatures if JWT_SECRET_KEY is matching.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 1. Try validating token with Supabase Client (most robust for Supabase auth integration)
    try:
        response = supabase.auth.get_user(token)
        if response and response.user:
            return CurrentUser(id=response.user.id, email=response.user.email)
    except Exception as e:
        # If Supabase validation fails, we try standard local HS256 JWT validation as fallback
        pass

    # 2. Local JWT decode fallback (useful for testing or custom logins)
    if JWT_SECRET_KEY:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            if user_id and email:
                return CurrentUser(id=user_id, email=email)
        except JWTError:
            pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
