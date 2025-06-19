from fastapi import APIRouter
from ..model import StartUp 

router = APIRouter(
    prefix= "/industries",
    responses={404: {"description": "Not found"}}
)

# Type i ketij array eshte Industry
industries = []




#get all startups
@router.get("/")
async def get():
    return {"industries" : industries}





