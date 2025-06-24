from fastapi import FastAPI
from .routers import startups
from .routers import users_router
from .routers import investments
from pydantic import BaseModel
from typing import Union




app = FastAPI()

app.include_router(startups.router)
app.include_router(users_router.router)
app.include_router(investments.router)


@app.get("/about")
def read_root():
    return {"Main page"}


import uvicorn
from fastapi import FastAPI 
from contextlib import asynccontextmanager

from src.commons.postgres import database


@asynccontextmanager
async def lifespan(app: FastAPI):
     await database.connect()
     yield
     await database.disconnect()

app = FastAPI()
app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
      uvicorn.run(app, host="0.0.0.0")











