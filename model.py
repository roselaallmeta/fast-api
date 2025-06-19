from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime


class StartUp(BaseModel):
    id : int
    created_at : datetime   # datetime is a type in pythohn , while timestamp is a type in mysql
    invested_at : datetime
    name : str
    description : str
    founders_name : str
    email : str
   # funding_stage : Enum
    website_url :str
    total_funding : float
    is_active : bool # bool is a python type , while boolean is a mysql type


class User(BaseModel): # si ta bej qe te identifikoj ca cdo user mund t bej - psh nj investitor ben x , nje founder ben x
    user_id : int
    user_name : str

class UserRoles(BaseModel):
    id : int
    #user_role : ENUM
    
        
class UserProfile(BaseModel):
    email: str
    #gender : ENUM
    phone_number : str
    created_at : datetime
    updated_at : datetime
    last_login : datetime
    is_active : bool


class Investment(BaseModel):
    id: int
    name: str
    amount: float
    equity_percent : float
    #currency : ENUM
    invested_on : datetime
    notes : str


class Industries(BaseModel):
    id : int
    name : str


class Team(BaseModel): # inseroje ne db
    id: int
    number_of_members : int
    names: str
    roles: str
    startup_before: bool
    




     
    



    













