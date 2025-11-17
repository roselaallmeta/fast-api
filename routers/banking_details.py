from typing import List
from fastapi import APIRouter, HTTPException
from ..model import BankingDetails
from ..src.commons.postgres import database


router = APIRouter(
    prefix="/bank-details", responses={404: {"description": "Not found"}}
)


# -------------------------------------------------------


async def insert_banking_details(banking_details: BankingDetails):
    query = "INSERT INTO main.banking_details (user_id, account_number, iban, bic, bank_name, bank_country, currency, balance, is_bank_verified) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING *"

    async with database.pool.acquire() as connection:
        await connection.fetchrow(
            query,
            banking_details.user_id,
            banking_details.account_number,
            banking_details.iban,
            banking_details.bic,
            banking_details.bank_name,
            banking_details.bank_country,
            banking_details.currency,
            banking_details.balance,
            banking_details.is_bank_verified)

        return {**banking_details.model_dump()}


@router.post("/")
async def post(banking_details: BankingDetails):
    return await insert_banking_details(banking_details)

# --------------------------------------------


async def get_banking_details(limit: int, offset: int) -> List:
    query = "SELECT * FROM main.banking_details LIMIT $1 OFFSET $2 "
    banking_details = []

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)

        if rows is None:
            raise HTTPException(
                status_code=404, detail="Banking details not found")

        for record in rows:
            entry = BankingDetails(
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

            banking_details.append({
                **entry.model_dump(),
                "id": record["id"]
            })

        return banking_details


@router.get("/")
async def get(limit: int = 10, offset: int = 0):
    return await get_banking_details(limit, offset)

# ------------------------------------------------


async def get_details_id(id: int, banking_details: BankingDetails):
    query = " SELECT * FROM main.banking_details WHERE id=$1"

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id)

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Could not find banking details with id={id}")

    banking_details = BankingDetails(
        user_id=row["user_id"],
        account_number=row["account_number"],
        iban=row["iban"],
        bic=row["bic"],
        bank_name=row["bank_name"],
        bank_country=row["bank_country"],
        currency=row["currency"],
        balance=row["balance"],
        is_bank_verified=row["is_bank_verified"]
    )

    return {
        "id": row["id"],
        **banking_details.model_dump()
    }


@router.get("/{id}", response_model=BankingDetails)
async def get_detail(id: int, banking_details: BankingDetails):
    return await get_details_id(id, banking_details)


# ----------------------------------------------------


async def put_banking_details(id: int, banking_details: BankingDetails):
    query = "UPDATE main.banking_details SET user_id=$2, account_number=$3, IBAN=$4, BIC=$5, bank_name=$6, bank_country=$7, currency=$8, balance=$9, is_bank_verified=$10  WHERE id= $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, id, banking_details.user_id, banking_details.account_number, banking_details.iban, banking_details.bic, banking_details.bank_name, banking_details.bank_country, banking_details.currency, banking_details.balance, banking_details.is_bank_verified)

        return {
            "message": "Banking details updated sucessfully",
            "user": {"id": id, **banking_details.model_dump()}
        }


@router.put("/{id}")
async def put(id: int, banking_details: BankingDetails):
    return await put_banking_details(id, banking_details)


# -------------------------------------------------------------------

async def delete_banking_details(id: int):
    query = "DELETE FROM main.banking_details WHERE id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(
            query,
            id
        )


@router.delete("/{id}")
async def delete(id: int):
    return await delete_banking_details(id)


# ---------------------------------------------------------------



