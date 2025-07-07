from typing import List
from fastapi import APIRouter, HTTPException
from ..model import BankingDetails
from ..src.commons.postgres import database



router = APIRouter(
    prefix="/banking_details", responses={404: {"description": "Not found"}}
)



@router.post("/")
async def insert_banking_details(banking_details: BankingDetails):
    query = """
INSERT INTO main.banking_details (
	user_id,
    account_number,
    bic,
    iban,
    bank_name,
    bank_country,
    currency,
    balance,
    is_bank_verified
) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
"""

    async with database.pool.acquire() as connection:
        await connection.execute(
            query,
            banking_details.user_id,
            banking_details.account_number,
            banking_details.bic,
            banking_details.iban,
            banking_details.bank_name,
            banking_details.bank_country,
            banking_details.currency,
            banking_details.balance,
            banking_details.is_bank_verified
        )


@router.get("/")
async def get_banking_details(limit: int, offset: int) -> List[BankingDetails]:
    
    query = """
        SELECT * FROM main.banking_details LIMIT $1 OFFSET $2 
    """

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)
        
        if rows is None:
            raise HTTPException(status_code=404, detail="Banking details not found")


        banking_details = [
            BankingDetails(
                #id=record["id"],
                user_id=record["user_id"],
				account_number=record["account_number"],
                iban=record["iban"],
                bic=record["bic"],
                bank_name=record["bank_name"],
                bank_country=record["bank_country"],
                currency=record["currency"],
                balance=record["balance"],
                is_bank_verified=record["is_bank_verified"]
            )
            for record in rows
        ]
        return banking_details




@router.delete("/")
async def delete_banking_details(banking_details: BankingDetails):
    query = "DELETE FROM main.banking_details WHERE (user_id = $1 AND account_number = $2 AND bic = $3 AND iban = $4 AND bank_name = $5 AND bank_country = $6 AND currency = $7 AND balance = $8 AND is_bank_verified = $9)"

    async with database.pool.acquire() as connection:
        await connection.execute(
    query,
    banking_details.user_id,
    banking_details.account_number,
    banking_details.bic,
    banking_details.iban,
    banking_details.bank_name,
    banking_details.bank_country,
    banking_details.currency,
    banking_details.balance,
    banking_details.is_bank_verified
)

#

















#@router.put("/")
# async def update_banking_details(
#     banking_details: BankingDetails,
# ) -> BankingDetails | None:
#     query = """
#     UPDATE main.banking_details
#     SET
#         account_number = $1,
#         bic = $2,
#         iban = $3,
#         bank_name = $4,
#         bank_country = $5,
#         currency = $6,
#         balance = $7,
#         is_bank_verified = $8
#     WHERE user_id = $9
#     RETURNING 
#         id,
#         account_number,
#         bic,
#         iban,
#         bank_name,
#         bank_country,
#         currency,
#         balance,
#         is_bank_verified
#     """

#     async with database.pool.acquire() as connection:
#         row = await connection.fetchrow(
#             query,
#             banking_details.account_number,
#             banking_details.bic,
#             banking_details.iban,
#             banking_details.bank_name,
#             banking_details.bank_country,
#             banking_details.currency,
#             banking_details.balance,
#             banking_details.is_bank_verified,
#             banking_details.user_id,
#         )

#         if row:
#             return BankingDetails(
#                 id=row["id"],
#                 account_number=row["account_number"],
#                 bic=row["bic"],
#                 iban=row["iban"],
#                 bank_name=row["bank_name"],
#                 bank_country=row["bank_country"],
#                 currency=row["currency"],
#                 balance=row["balance"],
#                 is_bank_verified=row["is_bank_verified"],
#             )

#         return None