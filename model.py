from fastapi import FastAPI
from pydantic import BaseModel


class StartUp(BaseModel):
    id : int
    name : str
    
    #description : str
    # industryId : enum



class User(BaseModel):
    id : int
    fullName : str
    email: str

    
    # birthday: date

    # founderId : str
    # description : str
    # industryId : enum


class Investment(BaseModel):
    id: int
    name: str
    amount: int






