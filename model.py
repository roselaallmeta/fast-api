from enum import Enum
from typing import Optional
from fastapi import FastAPI, File
from pydantic import BaseModel
from datetime import datetime


class Venture(BaseModel):
    id : int
    name : str
    created_at : datetime  # datetime is a type in pythohn , while timestamp is a type in mysql
    invested_at : datetime
    description : str
    founders_name : str
    email : str
   # funding_stage : Enum
    website_url :str
    total_funding : float
    is_active : bool # bool is a python type , while boolean is a mysql type


class StatusEnum(str, Enum): # kur rregjistrohet nje user/startup - 
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class User(BaseModel): # si ta bej qe te identifikoj ca cdo user mund t bej - psh nj investitor ben x , nje founder ben x
    user_id : int
    user_name : str
    #identification_document : File - file nuk eshte data type, beje tek endpointi
    identification_number : str
    date_of_birth : datetime

class UserRoles(BaseModel):
    id : int
    #user_role : ENUM
    
        
class UserProfile(BaseModel):
    email: str
    #gender : Enum
    phone_number : str
    created_at : datetime
    updated_at : datetime
    last_login : datetime
    is_active : bool


class Investment(BaseModel):
    id: int
    name: str
    date_of_birth : datetime
    #identification_document : Enum["Passport" , "national_id", "drivers license"]
    identification_number: str 
    capital_available : float
    amount_investing: float 
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


class Document(BaseModel):
    id: int
    name : str
    size: int
    issue_date : datetime
    expiry_date : datetime
    content : bytes # duhet ta besh ne databaze si longblob qe te ruhen te dhenat e dokumentit
    content_type: str
    uploaded_by: str # te jete mandatory- qe kur behet upload nje file te jete bashke me emrin e personit qe i ben upload
    uploaded_at: datetime #= Field(default_factory=datetime.timezone-aware)
    description: Optional[str] = None
    status: str # Optional[str] = Field(default="pending")
    


class BankingDetails(BaseModel):
    bank_account_number: str
    bic: str
    iban: str
    bank_name : str
    bank_country : str
    currency: enumerate
    is_bank_verified : bool




    




     
    



    













