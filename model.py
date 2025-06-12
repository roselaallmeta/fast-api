from fastapi import FastAPI
from pydantic import BaseModel


class StartUp(BaseModel):
    id : int
    name : str

    # founderId : str
    # description : str
    # industryId : enum



class User(BaseModel):
    id : int
    fullName : str
    
    # birthday: date

    # founderId : str
    # description : str
    # industryId : enum

