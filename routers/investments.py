from fastapi import APIRouter
from ..model import Investment 

router = APIRouter(
    prefix= "/investments",
    responses={404: {"description": "Not found"}}
)



# Type i ketij array eshte investments
investments = []



@router.post("/")
async def get(investment: Investment):
    investments.append(investment)

    return {"message" : "Investment has sucessfully been added."}



#get all investments
@router.get("/{id}")
async def get(id : int):
    for investment in investments:
        if (investment.id == id):
            return {"investment" : investment}

    return {"message" : "No such investment found."}



@router.get("/{name}")
async def get(name : str):
    for investment in investments:
        if (investment.name == name):
            return {"investment" : investment}

    return {"message" : "No such investment found."}



#delete an investment
@router.delete("/{id}")
async def delete(id: int):
    for investment in investments:
        if investment.id == id:
            investments.remove(investment)

            return {"message" : "Investment has been deleted."}

    return {"message" : "Investment not found"}



@router.delete("/{name}")
async def delete(name: str):
    for investment in investments:
        if investment.name == name:
            investments.remove(investment)

            return {"message" : "Investment has been deleted."}

    return {"message" : "Investment not found"}



@router.put("/{id}")
async def update(id: int , investment_new : Investment):
    for index, investment in enumerate(investments):
        if investment.id == id:
            investments[index] = investment_new
            return {"investment": investment_new}

    return {"No investment found to update."}



@router.put("/name/{name}")
async def update(name: str, investment_new : Investment):
    for index, investment in enumerate(investments):
        if investment.name == name:
            investments[index] = investment_new
            return {"investment": investment_new}

    return {"No investment found to update."}




















