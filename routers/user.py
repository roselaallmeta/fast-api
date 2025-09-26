from fastapi import APIRouter, HTTPException
from ..model import GenderEnum, User, UserRoleEnum
from ..src.commons.postgres import database
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


router = APIRouter(
    prefix="/users", responses={404: {"description": "Not found"}})

# -----------------------------------------------------------------------------

# async def get_all_users(limit: int, offset: int) -> List[User]:
#     query = "SELECT user_id, name, email, role, gender,password FROM main.users LIMIT $1 OFFSET $2"

#     async with database.pool.acquire() as connection:
#         rows = await connection.fetch(query, limit, offset)
#         users = [
#             User(
#                 user_id=record["user_id"],
#                 name=record["name"],
#                 email=record["email"],
#                 role=record["role"],
#                 gender=record["gender"],
#                 password=record["password"]
#             )
#             for record in rows
#         ]
#         return users

# @router.get("/?limit=10")
# async def get(limit: Optional[int] = 10, offset: Optional[int] = 0):
#     return await get_all_users(limit, offset)



@router.get("/{user_gender}")
async def get_gender_enum(user_gender: GenderEnum):

    if user_gender == {
        "female",
				"male",
				"other"
    }:
        return {"user_gender": user_gender}


@router.get("/{user_role}")
async def get_user_role(user_role: UserRoleEnum):

    if user_role == {
        "founder",
        "investor",
        "guest",
        "institution",
        "admin",
        "business"
    }:
        return {"user_role": user_role}
    


@router.get("/{user_id}")
async def get_user_id(user_id, user:User):
    return {"user_id": user_id}
        



    



# @router.get("/")
# async def filtered_user(user : User, skip: int = 0, limit : int = 10):


#  if gender == "male":
#     return {"message": "User is a male"}

#  if gender == "female":
#     return {"message": "User is a female"}

#  else :
#     return {"message": "Gender is undefined"}


# -----------------------------------------------------------------------------

async def insert_user(user: User):
    query = "INSERT INTO main.users (name, email, role, gender, password) VALUES ($1, $2, $3, $4, $5)"

    async with database.pool.acquire() as connection:
        await connection.execute(query, user.name, user.email, user.role, user.gender, user.password)

        return {**user, 'password': None}

   


# @router.post("/")
# async def post(user: User):
#     return await insert_user(user)

# -----------------------------------------------------------------------------


async def get_user_id(user_id: int):
    query = "SELECT * FROM main.users WHERE user_id = $1"

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, user_id)

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Could not find user with user_id={user_id}")

    return User(
        user_id=row["user_id"],
        name=row["name"],
        role=row["role"],
        email=row["email"],
        gender=row["gender"],
        password=row["password"]

    )


@router.get("/{user_id}", response_model=User)
async def get(user_id: str):
    return await get_user_id(user_id)

# -----------------------------------------------------------------------------


async def delete_user(user_id: int):
    query = "DELETE FROM main.users WHERE user_id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, user_id)

    return "User deleted sucessfully"


@router.delete("/{user_id}")
async def delete(user_id: str):
    return await delete_user(user_id)

# -----------------------------------------------------------------------------
