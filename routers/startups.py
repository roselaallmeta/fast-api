from fastapi import APIRouter, FastAPI, Query
from ..model import StartUp 
from typing import Annotated

#from app.db import get_connection



router = APIRouter(
    prefix= "/startups",
    responses={404: {"description": "Not found"}}
)



startups = []


#creating  a valid startup in the database
@router.post("/") 
async def create_startup(startup: StartUp):

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
                       INSERT INTO startups(id, name , created_at, invested_at , description, founders_name, email, website_url, total_funding, is_active) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s , %s)
                       """ (startup.id , startup.name , startup.created_at, startup.invested_at, startup.description, startup.founders_name, startup.email, startup.website_url, startup.total_funding, startup.is_active))
        
        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Startup successfully added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




#retrieve the startup by name 
@router.get("/{name}")
async def get_startup_name(
    name: str
):
    
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT name FROM startups WHERE name = %s"

    cursor.execute(query, (name,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return {"startup": result, "message": "Startup found"}
    else:
        raise HTTPException(status_code=404, detail="No startup with that name.")
    


@router.get("/{id}")
async def get_startup_id(
    id: int
):
    
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT id FROM startups WHERE id = %s"

    cursor.execute(query, (id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return {"startup": result, "message": "Startup found"}
    else:
        raise HTTPException(status_code=404, detail="No startup with that id.")
    



# te marr nje startup ta marresh  nga emri i founderit
@router.get("/{founders_name}")
async def get_founder_name(
    founders_name: str
):
    
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT founders_name FROM startups WHERE founders_name = %s"

    cursor.execute(query, (founders_name,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return {"founders_name": result, "message": "Startup found by founders name."}
    else:
        raise HTTPException(status_code=404, detail="No startup found.")


    


#get all startups as a list
@router.get("/")
async def get_startup():

    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM startups"

    cursor.execute(query)
    result = cursor.fetchall() 

    if result:
        return {"startups" : startups}

    else:
        raise HTTPException(status_code=404, detail="No startup listed.")
    

    # nje funksionalitet qe ti marri nga me i vjetri te me i riu




#updating a startup
@router.put("/update/{id}")
async def update(id : int , startup_new : StartUp):
    for index, startup in enumerate(startups):
        if startup.id == id:
            startups[index] = startup_new
            return {"startup": startup_new}

    return {"No startup found to update"}





# @router.put("/update/{id}")
# async def update_startup(id: int , updated_startup : dict):
#     for startup in startups:
#         if startup['id'] == id:

    





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

            

    
    
    

    
