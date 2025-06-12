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
    return {"users" : users}w



#creating a startup
@router.post("/") 
async def create(startup: User):
    users.append(startup)
    return {"message" : "Startup has sucessfully been added."}


#getting a single startup
@router.get("/{id}")
async def get(id : int): 
    for startup in users :
        if (startup.id == id):
            return {"startup" : startup}

    return {"message" : "No startup found."}


#deleting a single startup
@router.delete("/{id}")
async def delete(id : int):
    for startup in users:
        if startup.id == id:
            users.remove(startup)

            return {"message" : "Startup has been deleted"}
    
    return {"message" : "Startup not found"}



#updating a startup
@router.put("/{id}")
async def update(id : int , startup_new : StartUp):
    for startup in users :
        if startup.id == id:
            startup = startup_new

            return {"startup": startup}

    return {"No startup found to update"}
