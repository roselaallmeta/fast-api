from fastapi import APIRouter
from ..model import User 

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


#creating a user
@router.post("/") 
async def create(user: User):
    users.append(user)
    return {"message" : "User has sucessfully been added."}


#getting a single user
@router.get("/{id}")
async def get(id : int): 
    for user in users :
        if (user.id == id):
            return {"user" : user}

    return {"message" : "No user found."}


@router.get("/{fullName}")
async def get(fullName : str): 
    for user in users :
        if (user.fullName == fullName):
            return {"user" : user}

    return {"message" : "No user found."}


#deleting a single user
@router.delete("/{id}")
async def delete(id : int):
    for user in users:
        if user.id == id:
            users.remove(user)

            return {"message" : "User has been deleted"}
    
    return {"message" : "User not found"}


@router.delete("/{fullName}")
async def delete(fullName : str):
    for user in users:
        if user.fullName == fullName:
            users.remove(user)

            return {"message" : "User has been deleted"}

    return {"message" : "User not found"}


#updating a user
@router.put("/{id}")
async def update(id : int , user_new : User):
    for index, user in enumerate(users):
        if user.id == id:
            users[index] = user_new
            
            return {"user": user_new}

    return {"No user found to update"}



@router.put("/{fullName}")
async def update(fullName : str , user_new : User):
    for index, user in enumerate(users):
        if user.fullName == fullName:
            users[index] = user_new
            
            return {"user": user_new}

    return {"No user found to update"}



