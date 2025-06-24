from fastapi import APIRouter
from ..model import User 
from typing import List, Optional
from app import postgres
from src.users.users_schema import User


router = APIRouter(
    prefix= "/users",
    responses={404: {"description": "Not found"}}
)

# Type i ketij array eshte User
users = []


#get all users
@router.get("/")
async def get_users():
    return {"users" : users}


@router.get("/current")
async def read_user_me():
    return {"user_id": "the current user"}


#creating a user
@router.post("/") 
async def create(user: User):
    users.append(user)
    return {"message" : "User has sucessfully been added."}


#getting a single user
@router.get("/{user_id}")
async def get(user_id : int): 
    for user in users :
        if (user_id.id == id):
            return {"user" : user}

    return {"message" : "No user found."}


@router.get("/{user_name}")
async def get(user_name : str): 
    for user in users :
        if (user.user_name == user_name):
            return {"user" : user}

    return {"message" : "No user found."}


#deleting a single user
@router.delete("/{user_id}")
async def delete(id : int):
    for user in users:
        if user.user_id == user_id:
            users.remove(user)

            return {"message" : "User has been deleted"}
    
    return {"message" : "User not found"}


@router.delete("/{user_name}")
async def delete(user_name : str):
    for user in users:
        if user.user_name == user_name:
            users.remove(user)

            return {"message" : "User has been deleted"}

    return {"message" : "User not found"}


#updating a user
@router.put("/{user_id}")
async def update(user_id : int , user_new : User):
    for index, user in enumerate(users):
        if user.user_id == id:
            users[index] = user_new
            
            return {"user": user_new}

    return {"No user found to update"}



@router.put("/{user_name}")
async def update(user_name : str , user_new : User):
    for index, user in enumerate(users):
        if user.user_name == user_name:
            users[index] = user_new
            
            return {"user": user_new}

    return {"No user found to update"}



