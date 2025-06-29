from typing import List
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, File, UploadFile
from ..model import Investment
from datetime import date, timedelta
from ..database import get_connection



router = APIRouter(
    prefix= "/banking_details",
    responses={404: {"description": "Not found"}}
)



async def insert_banking_details(banking_details: BankingDetails):
    query = """
INSERT INTO main.banking_details (
    account_number,
    bic,
    iban,
    bank_name,
    bank_country,
    currency,
    balance,
    is_bank_verified
) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
"""

    
    async with database.pool.acquire() as connection:
        await connection.execute(query,
        banking_details.account_number,
        banking_details.bic,
        banking_details.iban,
        banking_details.bank_name,
        banking_details.bank_country,
        banking_details.currency,
        banking_details.balance,
        banking_details.is_bank_verified
    )
    

async def get_banking_details(banking_details: BankingDetails) -> BankingDetails | None:
    query = """
        SELECT 
            id,
            account_number,
            bic,
            iban,
            bank_name,
            bank_country,
            currency,
            balance,
            is_bank_verified
        FROM main.banking_details
        WHERE account_number = $1
    """
    
    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, banking_details.account_number)
        
        if row:
            return BankingDetails(
                id=row["id"],
                account_number=row["account_number"],
                bic=row["bic"],
                iban=row["iban"],
                bank_name=row["bank_name"],
                bank_country=row["bank_country"],
                currency=row["currency"],
                balance=row["balance"],
                is_bank_verified=row["is_bank_verified"]
            )
        
        return None
    



async def update_banking_details(banking_details: BankingDetails) -> BankingDetails | None:
    query = """
    UPDATE main.banking_details
    SET
        account_number = $1,
        bic = $2,
        iban = $3,
        bank_name = $4,
        bank_country = $5,
        currency = $6,
        balance = $7,
        is_bank_verified = $8
    WHERE user_id = $9
    RETURNING 
        id,
        account_number,
        bic,
        iban,
        bank_name,
        bank_country,
        currency,
        balance,
        is_bank_verified
    """
    
    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(
            query,
            banking_details.account_number,
            banking_details.bic,
            banking_details.iban,
            banking_details.bank_name,
            banking_details.bank_country,
            banking_details.currency,
            banking_details.balance,
            banking_details.is_bank_verified,
            banking_details.user_id
        )

        if row:
            return BankingDetails(
                id=row["id"],
                account_number=row["account_number"],
                bic=row["bic"],
                iban=row["iban"],
                bank_name=row["bank_name"],
                bank_country=row["bank_country"],
                currency=row["currency"],
                balance=row["balance"],
                is_bank_verified=row["is_bank_verified"]
            )

        return None

        

			
        



        
    

    


