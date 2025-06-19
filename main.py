from fastapi import FastAPI
from .routers import startups
from .routers import users
from .routers import investments
from pydantic import BaseModel
from typing import Union


app = FastAPI()

app.include_router(startups.router)
app.include_router(users.router)
app.include_router(investments.router)


@app.get("/about")
def read_root():
    return {"Main page"}
















