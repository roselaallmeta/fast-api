from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from ..model import User, UserProfile, Token, TokenData, UserLogin
from ..routers.user import get_user_id, get_user_name
from .auth import verify_password, get_password_hash, ph
from ..src.commons.postgres import database
 

router = APIRouter(
    prefix="/users", responses={404: {"description": "Not found"}}, tags=["auth"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token/login")
SECRET_KEY = 'cfedced76463b2836005fab76ab9748284e18e8a0c06344883c58314bc7838e0'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# @router.post("/")
# async def post(user: User):
#     return await create_user(user)


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
            password=row["password"]
        )

    return UserLogin(**user.model_dump())


# per te krijuar nje token- kemi header, payload dhe signature
# token is issued pasi ben log in sucessfully

# header = algorithm and type
# payload = data
# signature = secret key

async def create_access_token(data: dict, expire: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expire:
        exp = datetime.now(timezone.utc) + \
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        exp = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": exp})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


async def authenticate_user(username: str, password: str) -> UserLogin:
    user = await get_user_email(username)

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
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=user.email)
    except JWTError:
        raise credentials_exception
    user = await get_user_name(username=user.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[UserProfile, Depends(get_current_user)],
):
    if current_user.status == 'rejected':
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# nuk e definon si duhet te jet data te create_asccess_token, por e ben tek login_for_access_token


@router.post("/token/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = await authenticate_user(
        form_data.username, form_data.password)  # e definon sic e do forma
    
    if not user:
         raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await create_access_token(
        data={"sub": user.email}, 
        expire=access_token_expires,
    )
        
        
    return Token(access_token=access_token, token_type="bearer", id=user.id)



