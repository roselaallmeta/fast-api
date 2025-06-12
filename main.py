from fastapi import FastAPI
from model import StartUp

app = FastAPI()

@app.get("/about")
def read_root():
    return {"Main page."}

# Type i ketij array eshte StartUp
startups = []

#creating a startup
@app.post("/startup") 
async def create_startup(startup: StartUp):
    startups.append(startup)
    return {"message" : "Startup has sucessfully been added."}


#getting a single startup
@app.get("/startup/{id}")
async def get_startup(id : int): 
    for startup in startups :
        if (startup.startupId == id):
            return {"startup" : startup}

    return {"message" : "No startup found."}


#deleting a single startup
@app.delete("/startup/{id}")
async def delete_startup(id : int):
    for startup in startups:
        if startup.startupId == id:
            startups.remove(startup)
            return {"message" : "Startup has been deleted"}
    
    return {"message" : "Startup not found"}



#updating a startup
@app.put("/startups/{startupId}")
async def update_startup(startupId : int , startup_new : StartUp):
    for startup in startups :
        if startupId == id :
            startupId = id
            startup.startupName = startup_new.startupName
            return{"startup": startup}

    return {"No startup found to update"}

        
       

#get all startups
@app.get("/startup")
async def get_startups():
    return {"startups" : startups}

