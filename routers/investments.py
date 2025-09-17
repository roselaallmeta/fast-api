from typing import List
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, File, UploadFile
from ..model import Investment
from datetime import date, timedelta
from ..src.commons.postgres import database


router = APIRouter(prefix="/investments", responses={404: {"description": "Not found"}})


@router.post("/")
async def insert_investment(investment: Investment):
    query = """INSERT INTO main.investments(
    user_id,
    venture_id,
    title,
    amount,
    investment_type,
    equity_percent,
    currency,
    invested_on,
    description) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING *"""

    async with database.pool.acquire() as connection:
        row= await connection.fetchrow(
            query,
            investment.user_id,
            investment.venture_id,
            investment.title,
            investment.amount,
            investment.investment_type,
            investment.equity_percent,
            investment.currency,
            investment.invested_on,
            investment.description
        )
        

    return Investment(**row)
        
        
        
       
@router.get("/")
async def get_all_investments() -> List[Investment]:
    query = """
            SELECT
                    
                    user_id,
                    venture_id,
                    title,
                    amount,
                    investment_type,
                    equity_percent,
                    currency,
                    invested_on,
                    description
                FROM main.investments
            """

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query)
        
        investments = [
            Investment(
                #id=record["id"],
                user_id=record["user_id"],
                venture_id=record["venture_id"],
                title=record["title"],
                amount=record["amount"],
                investment_type=record["investment_type"],
                equity_percent=record["equity_percent"],
                currency=record["currency"],
                invested_on=record["invested_on"],
                description=record["description"]
            )
            for record in rows
           ]
        return investments
    
	

@router.get("/{id}", response_model=Investment)
async def get_investment_id(id: int):
    query = "SELECT * FROM main.investments WHERE id = $1"

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find investment with id={id}"
        )

    return Investment(
        user_id=row["user_id"],
        venture_id=row["venture_id"],
        title=row["title"],
        amount=row["amount"],
        investment_type=row["investment_type"],
        equity_percent=row["equity_percent"],
        currency=row["currency"],
        invested_on=row["invested_on"],
        description=row["description"]
    )

        




@router.put("/{id}", response_model=Investment)
async def update_investment(id:int, investment:Investment):
    query = """UPDATE main.investments SET 
    	user_id = $2,
        venture_id = $3,
        title = $4,
        amount = $5,
        investment_type = $6,
        equity_percent = $7,
        currency = $8,
        invested_on = $9,
        description = $10 WHERE id=$1 RETURNING *"""
    


    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id , 
                                        investment.user_id,
                                        investment.venture_id, 
                                        investment.title, investment.amount, 
                                        investment.investment_type, investment.equity_percent, 
                                        investment.currency, investment.invested_on, 
                                        investment.description)  

    if row is None:
        raise HTTPException(status_code=404, detail=f"Investment with id {id} does not exist")
    
    return Investment(
    user_id=row["user_id"],
    venture_id=row["venture_id"],
    title=row["title"],
    amount=row["amount"],
    investment_type=row["investment_type"],
    equity_percent=row["equity_percent"],
    currency=row["currency"],
    invested_on=row["invested_on"],
    description=row["description"]
)
    
        
        
    
    
    
    
    
    
    


@router.delete("/")
async def delete_investment(investment: Investment):
    query = """DELETE FROM main.investments WHERE 
    	user_id = $1 AND 
        venture_id = $2 AND
        title = $3 AND
        amount = $4 AND
        investment_type = $5 AND
        equity_percent = $6 AND
        currency = $7 AND
        invested_on = $8 AND
        description = $9
    ;
    """

    async with database.pool.acquire() as connection:
        await connection.execute(
            query,
            investment.user_id,
            investment.venture_id,
            investment.title,
            investment.amount,
            investment.investment_type,
            investment.equity_percent,
            investment.currency,
            investment.invested_on,
            investment.description
        )
        

    return {f"Investment deleted sucessfully."}






# @router.get("/{id}")
# async def get_investment_by_id(investment: Investment) -> Investment | None:
#     query = """
#         SELECT 
#             user_id, 
#             venture_id, 
#             title, 
#             amount, 
#             investment_type, 
#             equity_percent, 
#             currency, 
#             invested_on, 
#             description 
#         FROM main.investments 
#         WHERE id = $1
#     """

#     async with database.pool.acquire() as connection:
#         row = await connection.fetchrow(query, investment.id)
       
#         if row:
#             return Investment(
#                 id=row["id"],
#                 user_id=row["user_id"],
#                 venture_id=row["venture_id"],
#                 title=row["title"],
#                 amount=row["amount"],
#                 investment_type=row["investment_type"],
#                 equity_percent=row["equity_percent"],
#                 currency=row["currency"],
#                 invested_on=row["invested_on"],
#                 description=row["description"],
#             )
#         return None




@router.delete("/")
async def delete_investment(investment: Investment):
    query = """DELETE FROM main.investments WHERE user_id = $1 AND 
        venture_id = $2 AND
        title = $3 AND
        amount = $4 AND
        investment_type = $5 AND
        equity_percent = $6 AND
        currency = $7 AND
        invested_on = $8 AND
        description = $9
        WHERE id = $10);
    """

    async with database.pool.acquire() as connection:
        await connection.execute(
            query,
            investment.user_id,
            investment.venture_id,
            investment.title,
            investment.amount,
            investment.investment_type,
            investment.equity_percent,
            investment.currency,
            investment.invested_on,
            investment.description,
        )


# # Type i ketij array eshte investment
# investments = []


# def calculate_age(birthdate: date) -> int:
#     today = date.today()
#     return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


# def is_document_expired(expiry_date : date) -> bool:
#     today = date.today()
#     return expiry_date > today + timedelta(days=90)

# # timedelta(days=90) - a time period of 90 days
# # today + timedelta(days=90) - the date 90 days from now


# @router.post("/")  # per ta krijuar
# async def create_investment(investment : Investment, user: User): #async sepse po merr nga db
#     try:
#         connection = get_connection()
#         cursor = connection.cursor()

#         age = calculate_age(user.date_of_birth) # should date of birth also be declared in the investment model
#         if age < 18:
#             raise HTTPException(status_code=400, detail="Investor must be at least 18 years old.")


#         expiry = is_document_expired()


#         cursor.execute("""
#                        INSERT INTO investments(id, name , amount, equity_percent , currency, invested_on, notes)
#                        VALUES (%s, %s, %s, %s, %s, %s, %s)
#                        """ ,
#                        (investment.id ,
#                         investment.name,
#                         investment.amount,
#                         investment.equity_percent,
#                         investment.currency,
#                         investment.invested_on,
#                         investment.notes))


#         connection.commit()
#         cursor.close()
#         connection.close()


# 				# conditions
#                 # kur nje investor investon diku, - investor duhet te jete mbi 18 vjec qe te bej nje investim - done
#                 # i duhet te japi nje mjet identifikimi per t ber nje investim

#         return {"message": "Investment successfully added"}


#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/{name}")
# async def get_by_name(name : str):
#     for investment in investments:
#         if (investment.name == name):
#             return {"investment" : investment}

#     return {"message" : "No such investment found."}


# #get investment by id
# @router.get("/{id}")
# async def get_by_id(id : int):
#     for investment in investments:
#         if (investment.id == id):
#             return {"investment" : investment}

#     return {"message" : "No such investment found."}


# @router.get("/current{id}")
# async def get_current():
#     for investment in investments:
#         if investment.id == id.current_investment: # krijo nje metode per investimet e nje investitori qe te ket current_investment
#             return {"Current investments:" : current_investment}
#     return {"message" : "Could not find any investment."}


# @router.get("/current{name}")
# async def get_current():
#     for investment in investments:
#         if investment.name == name.current_investment: # krijo nje metode per investimet e nje investitori qe te ket current_investment
#             return {"Current investments:" : current_investment}
#     return {"message" : "Could not find any investment."}


# @router.put("/{id}") # per ti bere update me id e dhene
# async def update_id(id: int , investment_new : Investment):
#     for index, investment in enumerate(investments):
#         if investment.id == id:
#             investments[index] = investment_new
#             return {"investment": investment_new}

#     return {"No investment found to update."}


# @router.put("/{name}") # per ti bere update me emrin e dhene
# async def update_name(name: str, investment_new : Investment):
#     for index, investment in enumerate(investments):
#         if investment.name == name:
#             investments[index] = investment_new
#             return {"investment": investment_new}

#     return {"No investment found to update."}


# #delete an investment
# @router.delete("/{id}")
# async def delete(id: int):
#     for investment in investments:
#         if investment.id == id:
#             investments.remove(investment)

#             return {"message" : "Investment has been deleted."}

#     return {"message" : "Investment not found"}


# @router.delete("/{name}")
# async def delete(name: str):
#     for investment in investments:
#         if investment.name == name:
#             investments.remove(investment)

#             return {"message" : "Investment has been deleted."}

#     return {"message" : "Investment not found"}


# #delete nje investim nga founderi i startupit - kur te definosh qe nje user mund te jete nje founder
# @router.delete("/{founder.name}")
# async def delete(name: str):
#     for investment in investments:
#         if founder.name == name:
#             investments.remove(investment)

#             return {"message" : "Investment has been deleted."}

#     return {"message" : "Investment not found"}



# @router.put("/")
# async def update_investment(investment: Investment) -> Investment | None:
#     query = """
#         UPDATE main.investments
#         SET
#             title = $1,
#             amount = $2,
#             investment_type = $3,
#             equity_percent = $4,
#             currency = $5,
#             invested_on = $6,
#             description = $7,
#             user_id = $8,
#             venture_id = $9
#         WHERE id = $10
#         RETURNING id, user_id, venture_id, title, amount, investment_type, equity_percent, currency, invested_on, description
#     """

#     async with database.pool.acquire() as connection:
#         row = await connection.fetchrow(
#             query,
#             investment.title,
#             investment.amount,
#             investment.investment_type,
#             investment.equity_percent,
#             investment.currency,
#             investment.invested_on,
#             investment.description,
#             investment.user_id,
#             investment.venture_id,
#             investment.id,
#         )

#         if row:
#             return Investment(
#                 id=row["id"],
#                 user_id=row["user_id"],
#                 venture_id=row["venture_id"],
#                 title=row["title"],
#                 amount=row["amount"],
#                 investment_type=row["investment_type"],
#                 equity_percent=row["equity_percent"],
#                 currency=row["currency"],
#                 invested_on=row["invested_on"],
#                 description=row["description"],
#             )
        
#         return None