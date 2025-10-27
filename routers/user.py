from enum import Enum
from multiprocessing import connection
from multiprocessing.managers import BaseManager
from fastapi import APIRouter, Depends, HTTPException, Query
from ..model import GenderEnum, User, UserLogin, UserRoleEnum
from ..src.commons.postgres import database
from typing import List, Optional
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator


router = APIRouter(
    prefix="/users", responses={404: {"description": "Not found"}})

# -----------------------------------------------------------------------------


async def get_all_users(limit: int, offset: int) -> List:
    query = "SELECT id, name, email, role, password FROM main.users LIMIT $1 OFFSET $2"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)

        users = []

        for record in rows:
            user = User(
                id=record["id"],
                name=record["name"],
                email=record["email"],
                role=record["role"],
                password=record["password"]
            )

            users.append(user)

        return users


@router.get("/")
async def get(limit: int = 10, offset: int = 0):
    return await get_all_users(limit, offset)

# -----------------------------------------------------------------------------


async def create_user(user: User):
    query = "INSERT INTO main.users (name, email, role, password) VALUES ($1, $2, $3, $4) RETURNING id, name, email, role, created_at "

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, user.name, user.email, user.role, user.password)

        return row


@router.post("/")
async def post(user: User):
    return await create_user(user)

# -----------------------------------------------------------------------------


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
        password=row["password"]
    )

    return {
        **user.model_dump()
    }


@router.get("/{id}", response_model=User)
async def get_id(id: int):
    return await get_user_id(id)

# -----------------------------------------------------------------------------

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
    query = "UPDATE main.users SET name = $2, role = $3, email = $4, password = $5, gender = $6 WHERE user_id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, user_id, user.name, user.role, user.email, user.password, user.gender)

        return {
            "message": "User updated sucessfully",
            "user": {"id": user_id, **user.model_dump()}
        }


@router.put("/{user_id}")
async def put(user_id: int, user: User):
    return await update_user(user_id, user)

# -----------------------------------------------------

#bej return userId te personit qe ka ber login ose register



async def login(user: UserLogin):
    errors = []
    success = False

    if user.email == '':
        errors.append('Email not provided')

    if user.password == '':
        errors.append('Password not provided')
        

    query = "SELECT * FROM main.users WHERE email = $1 AND password = $2"
    async with database.pool.acquire() as connection:
        fetched_user = await connection.fetchrow(query, user.email, user.password)
        
        if fetched_user is None:
            errors.append('User not found')
            
        else:
            if user.password != fetched_user['password']:
                answer_error = errors.append('Password is invalid')
                print(answer_error)
                
            if user.email != fetched_user['email']:
                email_error =  errors.append('Email is invalid')
                print(email_error)
    
        if errors:
            return {"errors": errors, "success": success}
            
        success = True
        return {"errors": errors, "success": success, "user_id": user.id}
    

@router.post("/login")
async def user_login(user: UserLogin):
    return await login(user)

# --------------------------------------------------------------------

async def register_user(user: User): 
    errors = []
    success = False
    
    if user.role == None or user.role == '':
        errors.append('User role not provided')

    if user.email == None or user.email == '' or '@' not in user.email or '.' not in user.email:
        errors.append('Email not provided or is invalid')

    if user.password == None or user.password == '':
        errors.append('Password not provided')
       
    if errors:
        return {"errors": errors, "success": success}
        
            
    query = "INSERT INTO main.users (name, role, email, password) VALUES ($1, $2, $3, $4) RETURNING id"
    async with database.pool.acquire() as connection:
        user = await connection.execute(query, user.name, user.role, user.email, user.password)

        success = True
        return {"errors": errors, "success": success, "user_id": user.id }

    return user


@router.post("/register")
async def register(user: User):
    return await register_user(user)
  
# -----------------------------------------------------------------------------------




# ------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------

# async def forgot_password(user: User, password: str):
# 	query = "SELECT * FROM main.users WHERE password = $2"


# 	if password != user.password:
# 		return "Forgot password?"


# ------------------------------------------------
