from fastapi import APIRouter
from ..model import StartUp 

router = APIRouter(
    prefix= "/startups",
    responses={404: {"description": "Not found"}}
)

# Type i ketij array eshte StartUp
startups = []


#get all startups
@router.get("/")
async def get():
    return {"startups" : startups}


#creating a startup
@router.post("/") 
async def create(startup: StartUp):
    startups.append(startup)
    return {"message" : "Startup has sucessfully been added."}


#getting a single startup
@router.get("/{id}")
async def get(id : int): 
    for startup in startups :
        if (startup.id == id):
            return {"startup" : startup}

    return {"message" : "No startup found."}


#deleting a single startup
@router.delete("/{id}")
async def delete(id : int):
    for startup in startups:
        if startup.id == id:
            startups.remove(startup)

            return {"message" : "Startup has been deleted"}
    
    return {"message" : "Startup not found"}



#updating a startup
@router.put("/{id}")
async def update(id : int , startup_new : StartUp):
    for index, startup in enumerate(startups):
        if startup.id == id:
            startups[index] = startup_new
            return {"startup": startup_new}

    return {"No startup found to update"}
