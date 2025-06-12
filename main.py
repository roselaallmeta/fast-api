from fastapi import FastAPI
from model import StartUp

app = FastAPI()

@app.get("/about")
def read_root():
    return {"Main page."}

    