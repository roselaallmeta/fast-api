
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from ..src.commons.postgres import database
from ..model import Token, UserLogin
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pwdlib import PasswordHash


SECRET_KEY = 'cfedced7646354567b2836005fab76ab9748284e18e8a0c06344883c58314bc7838e0'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


ph = PasswordHash.recommended()


def verify_password(password, hashed_password):
    return ph.verify(password, hashed_password)

def get_password_hash(password):
    return ph.hash(password)

    
        
    
    
