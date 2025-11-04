from contextlib import asynccontextmanager
from fastapi import FastAPI
from .src.commons.postgres import database
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from .security import auth


from .routers import (
    user,
    ventures,
    teams,
    document,
    investments,
    pitch_decks,
    banking_details,
    venture_members,
    banking_details,
    user_profiles,
    team_members
)

from .security import (
    jwt_tokens
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
app.include_router(teams.router)
app.include_router(document.router)
app.include_router(investments.router)
app.include_router(pitch_decks.router)
app.include_router(banking_details.router)
app.include_router(venture_members.router)
app.include_router(user_profiles.router)
app.include_router(team_members.router)
app.include_router(user.router)
app.include_router(jwt_tokens.router)



@app.get("/")
def root():
    return {"message": "Server is running"}
