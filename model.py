from fastapi import FastAPI
from pydantic import BaseModel


class StartUp(BaseModel):

    startupId : int
    startupName : str


    #founderName : str
    #description : str
    #industry : enum

