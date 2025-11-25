from fastapi import APIRouter, Depends, HTTPException, Query
from enum import Enum
from multiprocessing import connection
from multiprocessing.managers import BaseManager
from ..model import GenderEnum, User, UserLogin, UserProfile, UserRoleEnum
from ..src.commons.postgres import database
from typing import List, Optional
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from ..security.permissions import RoleChecker, admin_required, investor_required, business_required, guest_required, founder_required, institution_required
import re
from ..security.auth import verify_password, get_password_hash




ph = PasswordHash.recommended()
reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#%])[A-Za-z\d@$#%]{6,20}$"
pat = re.compile(reg)


router = APIRouter(
    prefix="/users", responses={404: {"description": "Not found"}})


# -----------------------------------------------------------------------------

ph = PasswordHash.recommended()
password_pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#%])[A-Za-z\d@$#%]{6,20}$")

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)

#----------------------------------------------
async def register_user(user: User):
    errors = []

    if not user.name:
        errors.append("Name not provided")
    if not user.role:
        errors.append("User role not provided")
    if not user.email or '@' not in user.email or '.' not in user.email:
        errors.append("Email not provided or is invalid")
    if not user.hashed:
        errors.append("Password not provided")

    if user.hashed:
        if not password_pattern.fullmatch(user.hashed):
            errors.append("Password does not meet complexity requirements")

        hashed = get_password_hash(user.hashed)
        user.hashed = hashed
        
	
    if errors:
        return {"success": False, "errors": errors}


    query = """
        INSERT INTO main.users (name, role, email, hashed)
        VALUES ($1, $2, $3, $4)
        RETURNING id
    """
    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(
            query,
            user.name,
            user.role,
            user.email,
            user.hashed        
        )
        return row


@router.post("/register")
async def register(user: User):
    return await register_user(user)


#------------------------------------------

async def get_all_users(limit: int, offset: int, required_role:Annotated[bool, Depends(RoleChecker([UserRoleEnum.admin]))]) -> List:
    query = "SELECT id, name, email, role, hashed FROM main.users LIMIT $1 OFFSET $2"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)

        users = []

        for record in rows:
            user = User(
                id=record["id"],
                name=record["name"],
                email=record["email"],
                role=record["role"],
                hashed=record["hashed"]
            )

            users.append(user)

        return users
    

@router.get("/")
async def get(limit: int = 10, offset: int = 0, required_role=Depends(admin_required)):
    return await get_all_users(limit, offset, required_role)

#---------------------------------------------

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
        hashed=row["hashed"]
    )

    return {
        **user.model_dump()
    }


@router.get("/{id}", response_model=User)
async def get_id(id: int):
    return await get_user_id(id)

# ----------------------------------------------------------------


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
        hashed=row["hashed"]
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
    query = "UPDATE main.users SET name = $2, role = $3, email = $4, hashed = $5 WHERE user_id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, user_id, user.name, user.role, user.email, user.hashed)

        return {
            "message": "User updated sucessfully",
            "user": {"id": user_id, **user.model_dump()}
        }


@router.put("/{user_id}")
async def put(user_id: int, user: User):
    return await update_user(user_id, user)

# -----------------------------------------------------

