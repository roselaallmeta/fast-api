from fastapi import FastAPI
from .routers import startups
from .routers import users

app = FastAPI()
app.include_router(startups.router)
app.include_router(users.router)

@app.get("/about")

def read_root():
    return {"Main page - Rosi"}