from fastapi import APIRouter
from ..model import User 

router = APIRouter(
    prefix= "/user_profiles",
    responses={404: {"description": "Not found"}}
)

# Type i ketij array eshte User
users = []


#get all user profiles
@router.get("/")
async def get_user_profiles():
    return {"users" : users}


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