from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, File, UploadFile
from ..model import Investment
from datetime import date, timedelta
from ..database import get_connection



router = APIRouter(
    prefix= "/investments",
    responses={404: {"description": "Not found"}}
)




# Type i ketij array eshte investment
investments = []


def calculate_age(birthdate: date) -> int:
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


def is_document_expired(expiry_date : date) -> bool:
    today = date.today()
    return expiry_date > today + timedelta(days=90)

# timedelta(days=90) - a time period of 90 days
# today + timedelta(days=90) - the date 90 days from now

   

@router.post("/")  # per ta krijuar
async def create_investment(investment : Investment, user: User): #async sepse po merr nga db
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        age = calculate_age(user.date_of_birth) # should date of birth also be declared in the investment model
        if age < 18:
            raise HTTPException(status_code=400, detail="Investor must be at least 18 years old.")
        
        
        expiry = is_document_expired()


        cursor.execute("""
                       INSERT INTO investments(id, name , amount, equity_percent , currency, invested_on, notes) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)
                       """ ,
                       (investment.id , 
                        investment.name, 
                        investment.amount, 
                        investment.equity_percent,
                        investment.currency, 
                        investment.invested_on, 
                        investment.notes))
        

        connection.commit()
        cursor.close()
        connection.close()
        

				# conditions
                # kur nje investor investon diku, - investor duhet te jete mbi 18 vjec qe te bej nje investim - done
                # i duhet te japi nje mjet identifikimi per t ber nje investim

        return {"message": "Investment successfully added"}
    

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


    
    
   


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

























