from fastapi import APIRouter
from ..model import Investment 

router = APIRouter(
    prefix= "/investments",
    responses={404: {"description": "Not found"}}
)


# Type i ketij array eshte investment
investments = []

@router.post("/")  # per ta krijuar
async def create_investment(investment: Investment): #async sepse po merr nga db
    investments.append(investment)

    return {"message" : "Investment has sucessfully been added."}


@router.get("/{name}")
async def get_by_name(name : str):
    for investment in investments:
        if (investment.name == name):
            return {"investment" : investment}

    return {"message" : "No such investment found."}


#get investment by id
@router.get("/{id}")
async def get_by_id(id : int):
    for investment in investments:
        if (investment.id == id):
            return {"investment" : investment}

    return {"message" : "No such investment found."}



@router.get("/current{id}") 
async def get_current():
    for investment in investments:
        if investment.id == id.current_investment: # krijo nje metode per investimet e nje investitori qe te ket current_investment
            return {"Current investments:" : current_investment}
    return {"message" : "Could not find any investment."}  



@router.get("/current{name}") 
async def get_current():
    for investment in investments:
        if investment.name == name.current_investment: # krijo nje metode per investimet e nje investitori qe te ket current_investment
            return {"Current investments:" : current_investment}
    return {"message" : "Could not find any investment."} 




@router.put("/{id}") # per ti bere update me id e dhene
async def update_id(id: int , investment_new : Investment):
    for index, investment in enumerate(investments):
        if investment.id == id:
            investments[index] = investment_new
            return {"investment": investment_new}

    return {"No investment found to update."}



@router.put("/{name}") # per ti bere update me emrin e dhene
async def update_name(name: str, investment_new : Investment):
    for index, investment in enumerate(investments):
        if investment.name == name:
            investments[index] = investment_new
            return {"investment": investment_new}

    return {"No investment found to update."}




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






#delete nje investim nga founderi i startupit - kur te definosh qe nje user mund te jete nje founder
@router.delete("/{founder.name}")
async def delete(name: str):
    for investment in investments:
        if founder.name == name:
            investments.remove(investment)

            return {"message" : "Investment has been deleted."}

    return {"message" : "Investment not found"}

























