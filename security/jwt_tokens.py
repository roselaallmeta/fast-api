from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import ValidationError
from ..model import User, UserProfile, Token, TokenData, UserLogin, UserRoleEnum
# from ..routers.user import get_user_id, get_user_name
from .auth import verify_password, get_password_hash, ph
from ..src.commons.postgres import database


router = APIRouter(
    prefix="/users", responses={404: {"description": "Not found"}}, tags=["auth"])

refresh_tokens=[]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token/login")
SECRET_KEY = 'cfedced76463b2836005fab76ab9748284e18e8a0c06344883c58314bc7838e0'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 120




async def get_user_email(email: str) -> UserLogin | None:
    query = "SELECT * FROM main.users WHERE email = $1"
    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, email)

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Could not find user")

    if row:
        user = UserLogin(
            id=row["id"],
            email=row["email"],
            password=row["password"],
            role=row["role"]
        )

    return UserLogin(
        **user.model_dump(),
    )




#data -> the payload(claims) i want inside the token
async def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        exp = datetime.now(timezone.utc) + expires_delta
    else:
        exp = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": exp})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt  # ky eshte the created token




async def authenticate_user(email: str, password: str) -> UserLogin:
    user = await get_user_email(email)

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await get_user_email(email=email)
    if user is None:
        raise credentials_exception
    return user



async def get_current_active_user(
        current_user: Annotated[UserProfile, Depends(get_current_user)],
):
    if current_user.status == 'deactivated':
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user






async def validate_refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
      
    try:
        if token in refresh_tokens:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            role: str = payload.get("role")
            if email is None or role is None:
                raise credentials_exception
            
        else:
            raise credentials_exception
        

    except(JWTError, ValidationError):
        raise credentials_exception
    
    user = await get_user_email(email = email)
    
    if user is None:
        raise credentials_exception
    
    return user, token
        
    


@router.post("/token/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:

    user = await authenticate_user(
        form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

    access_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    access_token=create_token(data={"sub": user.email, "role": user.role}, 
		expires_delta = access_token_expires)
    
    refresh_token=create_token(data={"sub":user.email, "role": user.role}, expires_delta= refresh_token_expires)
    
    return Token(access_token=access_token, refresh_token=refresh_token)



#user, token 
@router.post("/token/refresh")
async def refresh_token(
    token_data: Annotated[tuple[UserProfile, str], Depends(validate_refresh_token)]
):
    user, token = token_data
    

    access_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_token(data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires)
    
    refresh_token= create_token(data={"sub": user.email, "role":user.role}, expires_delta=refresh_token_expires)
    
    refresh_tokens.remove(token)
    refresh_tokens.append(refresh_token)
    
    return Token(access_token=access_token , refresh_token=refresh_token)
    



    
    
    




  

        

    


