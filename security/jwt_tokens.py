from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import ValidationError
from ..model import ProfileStatusEnum, User, UserProfile, Token, TokenData, UserLogin, UserRoleEnum
from .auth import verify_password, get_password_hash, ph
from ..src.commons.postgres import database

router = APIRouter(
    prefix="/users", responses={404: {"description": "Not found"}}, tags=["auth"])


refresh_tokens = []
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token/login")
SECRET_KEY = 'cfedced76463b2836005fab76ab9748284e18e8a0c06344883c58314bc7838e0'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 120


# na duhet ta marrim si fillim by email sepse para se te bej log in nuk njihet nga id


async def get_user_email(email: str) -> UserLogin:
    query = "SELECT * FROM main.user_login WHERE email = $1 "

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, email)

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Could not find user with email={email}")

    return UserLogin(
        id=row["id"],
		    email=row["email"],
        name=row["name"],
        password=row["password"],
        role=row["role"]
		)
    

@router.get("/get-user-email/{email}", response_model=UserLogin)
async def get_email(email: str):
    return await get_user_email(email)

#---------------------------------------------
async def get_user_id(id: int):
    query = "SELECT * FROM main.users WHERE id = $1 "

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id)

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Could not find user with id={user.id}")

    user = User(
        id=row["id"],
        name=row["name"],
        role=row["role"],
        email=row["email"],
        hashed=row["hashed"],
        created_at=row["created_at"],
    )

    return {
        **user.model_dump()
    }


@router.get("/get-user-profile/{id}", response_model=User)
async def get_id(id: int):
    return await get_user_id(id)

#-------------------------------------------------------------

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


#---------------------------------------

async def authenticate_user(email: str, password: str):
    user = await get_user_email(email)

    query = "SELECT * FROM main.user_login WHERE email = $1 AND password = $2"
    async with database.pool.acquire() as connection:
        row = await connection.execute(query, email , password)

        if row is None:
            return False
        
    password_query = "SELECT ul.password , u.hashed FROM main.user_login ul INNER JOIN main.users u ON ul.id = u.id"
    async with database.pool.acquire() as connection:
        password_row = await connection.execute(password_query)
        
        if password_row is None:
            return False
             
    if not user: 
        return False
    
    if not verify_password(password_row.password, user.hashed):
        return False

    return user


#-------------------------------------------------

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

    user = await get_user_email(email = email)
    if user is None:
        raise credentials_exception
    return user


#----------------------------------------

async def get_current_active_user(
        current_user: Annotated[UserProfile, Depends(get_current_user)]
):
    if current_user.status in [ProfileStatusEnum.deactivated, ProfileStatusEnum.inactive]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user  


#-------------------------------------------------


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
    
    user = await get_user_email(email=email)
    
    if user is None:
        raise credentials_exception
    
    return user, token
        
    
#-------------------------------------

@router.post("/token/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:

    user = await authenticate_user(
        form_data.username, form_data.password
	)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

    access_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    access_token=await create_token(data={"sub": user["email"], "role": user["role"]}, 
		expires_delta = access_token_expires)

    refresh_token=await create_token(data={"sub":user["email"], "role": user["role"]}, expires_delta= refresh_token_expires)
    refresh_tokens.append(refresh_token)
   
    return Token(access_token=access_token, refresh_token=refresh_token)

#---------------------------------------

@router.post("/token/refresh")
async def refresh_token_function(
    token_data: Annotated[tuple[UserProfile, str], Depends(validate_refresh_token)]
):
    user, token = token_data
    
    access_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    access_token = await create_token(data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires)
    
    refresh_token= await create_token(data={"sub": user.email, "role":user.role}, expires_delta=refresh_token_expires)
    
    refresh_tokens.remove(token)
    refresh_tokens.append(refresh_token)
    
    return Token(access_token=access_token , refresh_token=refresh_token)
    



    
    
    




  

        

    


