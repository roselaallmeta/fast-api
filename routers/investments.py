from typing import List
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, File, UploadFile
from ..model import Investment
from datetime import date, timedelta
from ..src.commons.postgres import database


router = APIRouter(prefix="/investments",
                   responses={404: {"description": "Not found"}})


# ------------------------------------------------
async def get_investments(limit: int, offset: int) -> List:
    query = "SELECT * FROM main.investments LIMIT $1 OFFSET $2"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)

        investments = []

        for record in rows:
            investment = Investment(
                user_id=record["user_id"],
                venture_id=record["venture_id"],
                name=record["name"],
                amount=record["amount"],
                investment_type=record["investment_type"],
                equity_percent=record["equity_percent"],
                currency=record["currency"],
                invested_on=record["invested_on"],
                description=record["description"]
            )

            investments.append({
                **investment.model_dump(),
                "id": record["id"]
            })

        return investments


@router.get("/")
async def get_all_investments(limit: int = 10, offset: int = 0):
    return await get_investments(limit, offset)


# ----------------------------


async def get_investment_id(id: int):
    query = "SELECT * FROM main.investments WHERE id=$1"

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id)

        if row is None:
            raise HTTPException(
                status_code=404, detail=f"Could not find investment with id={id}")

        investment = Investment(
            user_id=row["user_id"],
            venture_id=row["venture_id"],
            name=row["name"],
            amount=row["amount"],
            investment_type=row["investment_type"],
            equity_percent=row["equity_percent"],
            currency=row["currency"],
            invested_on=row["invested_on"],
            description=row["description"]
        )

        return {
            **investment.model_dump(),
            "id": id,
        }


@router.get("/{id}")
async def get_investment(id: int):
    return await get_investment_id(id)


# -----------------------------------------------------


async def create_investment(investment: Investment):
    query = "INSERT INTO main.investments (user_id, venture_id, name, amount, investment_type, equity_percent, currency , invested_on , description) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING *"

    async with database.pool.acquire() as connection:
        await connection.fetchrow(query,
                                  investment.user_id,
                                  investment.venture_id,  investment.name, investment.amount, investment.investment_type, investment.equity_percent, investment.currency, investment.invested_on, investment.description)

        return {**investment.model_dump()}


@router.post("/")
async def create(investment: Investment):
    return await create_investment(investment)

# ------------------------------------------------------------------


async def delete_investment(id: int):
    query = "DELETE FROM main.investments WHERE id = $1"

    async with database.pool.acquire() as connection:
        await connection.fetchrow(query, id)

    return f"Investment with ID {id} has been deleted sucessfully."


@router.delete("/{id}")
async def delete(id: int):
    return await delete_investment(id)

# --------------------------------------------------------------------


async def update_investment(id: int, investment: Investment):
    query = "UPDATE main.investments SET user_id = $1, venture_id = $2, name = $3, amount = $4, investment_type = $5, equity_percent = $6, currency = $7, invested_on = $8, description = $9 WHERE id = $10"

    selectQuery = "SELECT * FROM main.investments WHERE id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, investment.user_id, investment.venture_id, investment.name, investment.amount, investment.investment_type, investment.equity_percent, investment.currency, investment.invested_on, investment.description, id)

        row = await connection.fetch(selectQuery, id)

        return {
            "message": "Investment updated sucessfully",
            "investment": {"id": id, **investment.model_dump()},
            "row": row
        }


@router.put("/{id}")
async def update(id: int, investment: Investment):
    return await update_investment(id, investment)

# --------------------
# investments/{user_id}


# mori te gjitha investimet dhe id e userit qe ka investuar aty
# krijoi nje array bosh me te gjitha investimet qe do ket ber useri -> do behen append aty

# duhet te kontrolloj nese user_id ne investment esht e njejt me id e userit

async def user_investments(id: int,user_id: int) -> List:
    query = "SELECT * FROM main.investments WHERE id =$1 AND user_id = $2 "

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, id,user_id)

        investments = []

        for record in rows:
            investment = Investment(
                user_id=record["user_id"],
                venture_id=record["venture_id"],
                name=record["name"],
                amount=record["amount"],
                investment_type=record["investment_type"],
                equity_percent=record["equity_percent"],
                currency=record["currency"],
                invested_on=record["invested_on"],
                description=record["description"]
            )

            investments.append({
                **investment.model_dump(),
                "user_id": record["user_id"]
            })

        return investments

# investments / id e investimit /user-investment/  user_id
@router.get("/{id}/user-investment/{user_id}")
async def get_all_user_investments(id: int, user_id: int):
    return await user_investments(id, user_id)
