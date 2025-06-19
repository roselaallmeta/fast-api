from fastapi import APIRouter, FastApi, Query
from ..model import StartUp 
from typing import Annotated



router = APIRouter(
    prefix= "/startups",
    responses={404: {"description": "Not found"}}
)

# Type i ketij array eshte StartUp
# startups = [

#     {   'id': 1 ,
#         'name' : 'chatgpt' , 
#         'description' : 'some text' , 
#         'founders_name' : 'sam' , 
#         'email' : 'test@gmail.com' , 
#         'website_url ' : 'fjnjdnjn' , 
#         'total_funding': 3324.2 , 
#         'is_active' : 'true'},


#     {   'id': 2 ,
#         'name' : 'n28' , 
#         'description' : 'some text 2' , 
#         'founders_name' : 'some guy' , 
#         'email' : 'test2@gmail.com' , 
#         'website_url ' : 'fxkkxjn' , 
#         'total_funding': 578754.3 , 
#         'is_active' : 'false'}

# ]



@router.get("/{name}")
async def get_startup_name(
    name: Annotated[str, Path(min_length=2)]
):
    
    connection = get_connection()
    cursor = conn.cursor()
    query = "SELECT name FROM startups WHERE name = %s"

    cursor.execute()



   
    



    


    



#get all startups
@router.get("/")
async def get_startup():

    cursor.execute(SELECT * FROM startups)
    return {"startups" : startups} # ti kthej si liste - me id , name , dhe cdo atribut qe ka




#getting a single startup
@router.get("/{id}")
async def get_startup(id: int): 

    cursor.execute(SELECT id FROM startups)
    for startup in startups:
        if (startup.id == id):
            return {"startup by its id" : startup}

    return {"message" : "No startup found."}



#creating a startup
@router.post("/") 
async def create(startup: StartUp):
    startups.append(startup)
    return {"message" : "Startup has sucessfully been added."}



#updating a startup
@router.put("/update/{id}")
async def update(id : int , startup_new : StartUp):
    for index, startup in enumerate(startups):
        if startup.id == id:
            startups[index] = startup_new
            return {"startup": startup_new}

    return {"No startup found to update"}


@router.put("/update/{id}")
async def update_startup(id: int , updated_startup : dict):
    for startup in startups:
        if startup['id'] == id:






@router.delete("/{name}")
async def delete_startup_name(name : str):
    for startup in startups:
        if startup.name == name:
            startups.remove(startup)
            return {"StartUp sucessfully deleted by its name."}
        

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Startup not found"
    )
    




#deleting a single startup
@router.delete("/{id}")
async def delete(id : int):
    for startup in startups:
        if startup.id == id:
            startups.remove(startup)

            return {"message" : "Startup has been deleted"}
        


    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Startup not found"
    )


    
    #return {"message" : "Startup not found"} - this doesnt do anything , use raise

            

    
    
    

    
