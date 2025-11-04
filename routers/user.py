from fastapi import APIRouter, Depends, HTTPException, Query
from enum import Enum
from multiprocessing import connection
from multiprocessing.managers import BaseManager
from ..model import GenderEnum, User, UserLogin, UserRoleEnum
from ..src.commons.postgres import database
from typing import List, Optional
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash



ph = PasswordHash.recommended()


router = APIRouter(
    prefix="/users", responses={404: {"description": "Not found"}})

# -----------------------------------------------------------------------------

async def register_user(user: User):
    errors = []
    success = False
    
    hashed = ph.hash(user.hashed_password)

    if user.name == None or user.name == '':
        errors.append('User name not provided')

    if user.role == None or user.role == '':
        errors.append('User role not provided')

    if user.email == None or user.email == '' or '@' not in user.email or '.' not in user.email:
        errors.append('Email not provided or is invalid')
		
    if user.hashed_password == None or user.hashed_password == '':
        errors.append('Password not provided')

    if errors:
        return {"errors": errors, "success": success}

    query = "INSERT INTO main.users (name, role, email, hashed_password) VALUES ($1, $2, $3, $4) RETURNING id"
    
    async with database.pool.acquire() as connection:
        user = await connection.execute(query, user.name, user.role, user.email, hashed)

        success = True
        return {"errors": errors, 
                "success": success}

    return user


@router.post("/register")
async def register(user: User):
    return await register_user(user)



#----------------------------------------------------------------------------


async def get_all_users(limit: int, offset: int) -> List:
    query = "SELECT id, name, email, role, hashed_password FROM main.users LIMIT $1 OFFSET $2"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)

        users = []

        for record in rows:
            user = User(
                id=record["id"],
                name=record["name"],
                email=record["email"],
                role=record["role"],
                hashed_password=record["hashed_password"]
            )

            users.append(user)

        return users


@router.get("/")
async def get(limit: int = 10, offset: int = 0):
    return await get_all_users(limit, offset)

# -----------------------------------------------------------------------------


async def create_user(user: UserLogin):
    query = "INSERT INTO main.users (name, email, role, hashed_password) VALUES ($1, $2, $3, $4) RETURNING id, name, email, role, created_at "
  
    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, user.name, user.email, user.role, user.hashed_password)
       

        return row




#------------------------------------------------------------------------------

async def get_user_id(id: int):
    query = "SELECT * FROM main.users WHERE id = $1"

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id)

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Could not find user with id={id}")

    user = User(
        id=row["id"],
        name=row["name"],
        role=row["role"],
        email=row["email"],
        hashed_password=row["hashed_password"]
    )

    return {
        **user.model_dump()
    }


@router.get("/{id}", response_model=User)
async def get_id(id: int):
    return await get_user_id(id)

# -----------------------------------------------------------------------------


async def get_user_name(name: str):
    query = "SELECT * FROM main.users WHERE name = $1"

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, name)

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Could not find user")

    user = UserLogin(
        id=row["id"],
        name=row["name"],
        hashed_password=row["hashed_password"]
    )
    
    return {
        **user.model_dump()
    }


# --------------------------------------
async def delete_user(id: int):
    query = "DELETE FROM main.users WHERE user_id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, id)

    return f"User with ID {id} has been deleted sucessfully."


@router.delete("/{id}")
async def delete(id: int):
    return await delete_user(id)

# -----------------------------------------------------------------------------


async def update_user(user_id: int, user: User):
    query = "UPDATE main.users SET name = $2, role = $3, email = $4, hashed_password = $5 WHERE user_id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, user_id, user.name, user.role, user.email, user.hashed_password)

        return {
            "message": "User updated sucessfully",
            "user": {"id": user_id, **user.model_dump()}
        }


@router.put("/{user_id}")
async def put(user_id: int, user: User):
    return await update_user(user_id, user)

# -----------------------------------------------------

# bej return userId te personit qe ka ber login ose register



# --------------------------------------------------------------------------------

# async def forgot_password(user: User, password: str):
# 	query = "SELECT * FROM main.users WHERE password = $2"


# 	if password != user.password:
# 		return "Forgot password?"


# ------------------------------------------------
