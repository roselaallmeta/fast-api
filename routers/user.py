from fastapi import APIRouter, HTTPException
from ..backend.model import User
from ..src.commons.postgres import database
from typing import List, Optional



router = APIRouter(prefix="/users", responses={404: {"description": "Not found"}})

@router.get("/")
async def get_all_users(limit: int, offset: int) -> List[User]:
    query = "SELECT user_id, name, email, role, gender FROM main.users LIMIT $1 OFFSET $2"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)
        users = [
            User(
                user_id=record["user_id"],
                name=record["name"],
                email=record["email"],
                role=record["role"],
                gender=record["gender"]
            )
            for record in rows
        ]
        return users
    




@router.get("/{user_id}", response_model=User)
async def get_user_id(user_id: int):
    query = "SELECT * FROM main.users WHERE user_id = $1"
    
    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, user_id)
        
    if row is None:
            raise HTTPException(status_code=404, detail=f"Could not find user with user_id={user_id}")
    

    return User(
        user_id=row["user_id"],
        name=row["name"],
        role=row["role"],
        email=row["email"],
        gender=row["gender"]    
	)
             
        

@router.post("/")
async def insert_user(user: User):
    query = "INSERT INTO main.users (name, email, gender, role) VALUES ($1, $2, $3, $4)"

    async with database.pool.acquire() as connection:
        await connection.execute(query, user.name, user.email, user.gender, user.role)




@router.put("/{user_id}" , response_model=User)
async def update_user_id(user_id : int, user:User):
    query = "UPDATE main.users SET name = $2, role = $3, " \
			"email = $4 , gender = $5 WHERE user_id = $1 RETURNING *"
    
    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(
            query,
            user_id,
            user.name,
            user.role,
            user.email,
            user.gender
        ) 

    if row is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} does not exist")
    
    return User(
    name=row["name"],
    role=row["role"],
    email=row["email"],
    gender=row["gender"]
	)
    



@router.delete("/{user_id}")
async def delete_user(user_id : int):
    query = "DELETE FROM main.users WHERE user_id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, user_id)
        
    return "User deleted sucessfully";



# -----------------------------------------


@router.get("/{role}")
# async def get_users_by_role(limit: int, offset: int) -> List[User]:
#     query = "SELECT name, email, role, gender FROM main.users WHERE role = $1"

#     async with database.pool.acquire() as connection:
#         rows = await connection.fetch(query, limit, offset)
#         users = [
#             User(
#                 name=record["name"],
#                 email=record["email"],
#                 role=record["role"],
#                 gender=record["gender"],
#             )
#             for record in rows
#         ]
#         return users


# @router.get("/{id}")
# async def get_user_by_id(limit: int, offset: int) -> User:
#     query = "SELECT name, email, role, gender FROM main.users LIMIT $1 OFFSET $2"

#     async with database.pool.acquire() as connection:
#         rows = await connection.fetchrow(query, limit, offset)
#         users = [
#             User(
#                 name=record["name"],
#                 email=record["email"],
#                 role=record["role"],
#                 gender=record["gender"],
#             )
#             for record in rows
#         ]
#         return users





# @router.put("/")
# async def update_user(user: User) -> User | None:
#     query = "UPDATE main.users SET name = $1, email = $2, gender = $3, role = $4 WHERE id = $5"

#     async with database.pool.acquire() as connection:
#         row = await connection.fetchrow(
#             query, user.name, user.email, user.gender, user.role
#         )
#         if row:
#             return User(
#                 name=row["name"],
#                 email=row["email"],
#                 role=row["role"],
#                 gender=row["gender"],
#             )
#         return None




@router.get("/")
async def get(limit: Optional[int] = 10, offset: Optional[int] = 0):
    return await get_all_users(limit, offset)


@router.post("/")
async def post(user: User):
    return await insert_user(user)

    # query = "SELECT name, email FROM users WHERE email = $1"
    # async with database.pool.acquire() as connection:
    #     row = await connection.fetchrow(query, email)
    #     if row is not None:
    #         user = User(name=row["name"], email=row["email"])
    #         return user
    #     return None


# @router.get("/{id}")
# async def get_user(user_id: int, id: Annotated[str, Depends(get_db_connection)]):
#     row = await conn.fetchrow("SELECT FROM users WHERE id = $1", user_id)
#     if row is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return dict(row)


# @router.delete("/{id}")
# async def delete_user(user_id: int, id: Annotated[str, Depends(get_db_connection)]):
#     row = await conn.fetchrow("DELETE FROM users WHERE id = $1", user_id)
#     if row is None:
#         raise HTTPException(status_code=404, detail="Could not delete user")
#     return dict(row)


# #updates
# @router.put("/{id}")


# @router.delete("/")
# async def delete_users(user: User,Depend(get_db_connection)):
#     result = await conn.execute("DELETE FROM users")
#     if row is None:
#         raise HTTPException(status_code=404, detail="Could not delete users")
#     return [dict(row) for row in rows]


# @router.get("/{name}")
# async def get_user(user_name: str, name: Annotated[str, Depends(get_db_connection)]):
#     row = await conn.fetchrow("SELECT FROM users WHERE name = $1", user_name)
#     if row is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return dict(row)


# @router.get("/")
# async def get_user(user: User, Depends(get_db_connection)):
#     row = await conn.fetchrow("SELECT * FROM users")
#     if row is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return [dict(row) for row in rows]

# #getting a single user
# @router.get("/{user_id}")
# async def get(user_id : int):
#     for user in users :
#         if (user_id.id == id):
#             return {"user" : user}

#     return {"message" : "No user found."}


# @router.get("/{user_name}")
# async def get(user_name : str):
#     for user in users :
#         if (user.user_name == user_name):
#             return {"user" : user}

#     return {"message" : "No user found."}


# #deleting a single user
# @router.delete("/{user_id}")
# async def delete(id : int):
#     for user in users:
#         if user.user_id == user_id:
#             users.remove(user)

#             return {"message" : "User has been deleted"}

#     return {"message" : "User not found"}


# @router.delete("/{user_name}")
# async def delete(user_name : str):
#     for user in users:
#         if user.user_name == user_name:
#             users.remove(user)

#             return {"message" : "User has been deleted"}

#     return {"message" : "User not found"}


# #updating a user
# @router.put("/{user_id}")
# async def update(user_id : int , user_new : User):
#     for index, user in enumerate(users):
#         if user.user_id == id:
#             users[index] = user_new

#             return {"user": user_new}

#     return {"No user found to update"}


# @router.put("/{user_name}")
# async def update(user_name : str , user_new : User):
#     for index, user in enumerate(users):
#         if user.user_name == user_name:
#             users[index] = user_new

#             return {"user": user_new}

#     return {"No user found to update"}
