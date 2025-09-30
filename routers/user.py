from enum import Enum
from multiprocessing import connection
from fastapi import APIRouter, HTTPException, Query
from ..model import GenderEnum, User, UserRoleEnum
from ..src.commons.postgres import database
from typing import List, Optional
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator, validator



router = APIRouter(
		prefix="/users", responses={404: {"description": "Not found"}})

# -----------------------------------------------------------------------------


async def get_all_users(limit: int, offset: int) -> List:
		query = "SELECT user_id, name, email, role, gender, password FROM main.users LIMIT $1 OFFSET $2"

		async with database.pool.acquire() as connection:
				rows = await connection.fetch(query, limit, offset)

				users = []

				for record in rows:
						user = User(
								name=record["name"],
								email=record["email"],
								role=record["role"],
								gender=record["gender"],
								password=record["password"]
						)

						users.append({
								**user.model_dump(),
								"user_id": record["user_id"]
						})

				return users


@router.get("/")
async def get(limit: int = 10, offset: int = 0):
		return await get_all_users(limit, offset)

# -----------------------------------------------------------------------------


async def create_user(user: User):
		query = "INSERT INTO main.users (name, email, role, gender, password) VALUES ($1, $2, $3, $4, $5)"

		async with database.pool.acquire() as connection:
				await connection.execute(query, user.name, user.email, user.role, user.gender, user.password)

				return {**user.model_dump(), 'password': None}


@router.post("/")
async def post(user: User):
		return await create_user(user)

# -----------------------------------------------------------------------------


async def get_user_id(user_id: int):
		query = "SELECT * FROM main.users WHERE user_id = $1"

		async with database.pool.acquire() as connection:
				row = await connection.fetchrow(query, user_id)

		if row is None:
				raise HTTPException(
						status_code=404, detail=f"Could not find user with user_id={user_id}")

		user = User(
				name=row["name"],
				role=row["role"],
				email=row["email"],
				gender=row["gender"],
				password=row["password"]
		)

		return {
				"user_id": row["user_id"],
				**user.model_dump()
		}


@router.get("/{user_id}", response_model=User)
async def get_id(user_id: int):
		return await get_user_id(user_id)

# -----------------------------------------------------------------------------


async def delete_user(user_id: int):
		query = "DELETE FROM main.users WHERE user_id = $1"

		async with database.pool.acquire() as connection:
				await connection.execute(query, user_id)

		return f"User with ID {user_id} has been deleted sucessfully."


@router.delete("/{user_id}")
async def delete(user_id: int):
		return await delete_user(user_id)

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

#-----------------------------------------------------


async def login(email: str, password: str):
	errors = []
	success = False

	if email == None or email == '':
		errors.append('Email not provided')
		return { "errors": errors, "success": success }
	
	if password == None or password == '':
		errors.append('Password not provided')
		return { "errors": errors, "success": success }

	query = "SELECT * FROM main.users WHERE email = $1 LIMIT 1"

	async with database.pool.acquire() as connection:
			user = await connection.fetchrow(query, email)

			if user == None:
				errors.append('User not found')
				return { "errors": errors, "success": success }

			if user.password != password:
				errors.append('Password is invalid')
				return { "errors": errors, "success": success }

			success = True
			return { "errors": errors, "success": success }


@router.post("/login")
async def user_login(body):
	return body
	# return await login(email, password)
		
		# @field_validator("email")
		# async def email_validator():
		 
		 
		 
					
			
		
	
