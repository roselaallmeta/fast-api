from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, FastAPI
from ..src.commons.postgres import database
from ..model import Token, UserLogin, UserRoleEnum
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pwdlib import PasswordHash
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware



SECRET_KEY = 'cfedced7646354567b2836005fab76ab9748284e18e8a0c06344883c58314bc7838e0'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ph = PasswordHash.recommended()
# hashed = ph.hash(user.password)

def verify_password(password, hashed):
    return ph.verify(password, hashed)

def get_password_hash(password):
    return ph.hash(password) 



@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()
    
app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )



# RESOURCES_FOR_ROLES = {
    
#     "admin": {
#         'users': ['read', 'write', 'delete'],
#         'investors': ['read', 'write', 'delete'],
#         'ventures': ['read', 'write', 'delete'],
#         'teams': ['read', 'write', 'delete'],  
#     },
    
#     "founder": {
#         'teams': ['read', 'write', 'delete', 'update'],
#         'members': ['read'],
#         'investments': ['read'], 
#         'pitch_decks': ['read', 'write'],
#     },
    
# 		"business": {
#         'teams': ['read', 'write', 'delete', 'update'],
#         'members': ['read'],
#         'investments': ['read'], 
#         'pitch_decks': ['read', 'write'],
#     },
    
# 		"investor": {
#         'ventures': ['read', 'update'], # update -> to invest
#         'teams': ['read', 'update'], 
#         'members': ['read'],
#         'investments': ['read'], 
#         'pitch_decks': ['read'],
#     },
    
# 		"institution": {
#         'ventures': ['read'],
#         'teams': ['read'],
#         'members': ['read'],
#         'investments': ['read'], 
#         'pitch_decks': ['read'],
#     },
    
# 		"guest" : {
#         'ventures': ['read'], 
#         'teams': ['read'],
# 		},
# }


# USERS = {
#     'user1': {'username': 'user1', 'password': 'password', 'role': 'user'},
#     'admin1': {'username': 'admin1', 'password': 'adminpassword', 'role': 'admin'}
# }

# EXLUDED_PATHS = ['docs', 'openapi.json']


# def translate_method_to_action(method: str) -> str:
#     method_permission_mapping = {
#         'GET': 'read',
#         'POST': 'write',
#         'PUT': 'update',
#         'DELETE': 'delete',
# 		}
#     return method_permission_mapping.get(method.upper(), 'read')
    

# def has_permission(role, resource_name, required_permission):
#     if role in RESOURCES_FOR_ROLES and resource_name in RESOURCES_FOR_ROLES[role]:
#         return required_permission in RESOURCES_FOR_ROLES[role][resource_name]
#     return False

# class RBACMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         request_method = str(request.method).upper()
#         action = translate_method_to_action(request_method)
#         resource = request.url.path[1:]
#         if not resource in EXLUDED_PATHS:
#             admin1 = USERS['admin1'] # Switch between user and admin by commenting out this or the next line
#             #user1 = USERS['user1'] 
#             if not has_permission(admin1['role'], resource, action):
#                 raise HTTPException(status_code=403, detail="Insufficient permissions")
#         response = await call_next(request)
#         return response
        


