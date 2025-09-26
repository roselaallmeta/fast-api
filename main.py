from contextlib import asynccontextmanager
from fastapi import FastAPI
from .src.commons.postgres import database
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from .routers import (
    user,
    ventures,
    pitch_decks,
    banking_details,
    document,
    investments,
    user_profiles,
    venture_members
)


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

app.include_router(user.router)
app.include_router(ventures.router)
app.include_router(pitch_decks.router)
app.include_router(banking_details.router)
app.include_router(document.router)
app.include_router(investments.router)
app.include_router(user_profiles.router)
app.include_router(venture_members.router)


@app.get("/")
def root():
    return {"message": "Server is running"}


@app.get("/items")
async def get(take: int, skip: int):
    return {"items": [], "take": take, "skip": skip}

# @app.post("/")
# async def create_user(user):
#     user_dict = user.dict()
#     if [user.name, user.email, user.password, user.role, user.gender] is not None:
#         return {"message": "User created successfully"}

    # success == true;
    # errors = [];


# @app.post("/users")
# async def fetch_user(res):
#    request_body = {user.name, user.email, user.password, user.role, user.gender};


#    res = await request_body.post("http://localhost:8000")
#    return await res.json();


# app.include_router(industries.router)
# app.include_router(investment_validation.router)
# app.include_router(user_profiles.router)
# app.include_router(investments.router)
# app.include_router(user_profiles.router)


# if __name__ == "__main__ ":
#     uvicorn.run(app, host="0.0.0.0", port=8002)
