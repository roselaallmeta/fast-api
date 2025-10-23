from enum import Enum
from multiprocessing import connection
from fastapi import APIRouter, HTTPException, Query
from ..model import Venture, User
from ..src.commons.postgres import database
from typing import List, Optional
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


router = APIRouter(
    prefix="/ventures", responses={404: {"description": "Not found"}})

# -----------------------------------------------------------------------------


async def get_all_ventures(limit: int, offset: int) -> List:
    query = "SELECT id, name, created_at, phone_number, email, description,industries, funding_stage, website_url, funding_goal, total_funding, valuation, status FROM main.ventures LIMIT $1 OFFSET $2"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)

        ventures = []

        for record in rows:
            venture = Venture(
                name=record["name"],
                created_at=record["created_at"],
                phone_number=record["phone_number"],
                email=record["email"],
                description=record["description"],
                industries=record["industries"],
                funding_stage=record["funding_stage"],
                website_url=record["website_url"],
                funding_goal=record["funding_goal"],
                total_funding=record["total_funding"],
                valuation=record["valuation"],
                status=record["status"]
            )

            ventures.append({
                "id": record["id"],
                **venture.model_dump()
            })

        return ventures


@router.get("/")
async def get_ventures(limit: int, offset: int):
    return await get_all_ventures(limit, offset)


# -----------------------------------------------------------------------------


# async def add_member(id: int, member: Venture):
#     query = "INSERT INTO main.ventures(name, phone_number, email, description, industries, funding_stage, website_url , funding_goal, total_funding, valuation, is_active) VALUES ($1, $2, $3, $4, $5, $6 ,$7 ,$8 ,$9 ,$10, $11) RETURNING *"

#     async with database.pool.acquire() as connection:
#         await connection.fetchrow(query,
#                                   member.name,
#                                   member.phone_number,
#                                   member.email,
#                                   member.description,
#                                   member.industries,
#                                   member.funding_stage,
#                                   member.website_url,
#                                   member.funding_goal,
#                                   member.total_funding,
#                                   member.valuation,
#                                   member.is_active)

#         return {**member.model_dump()}


# @router.post("/{id}/members")
# async def post(venture: Venture):
#     return await create_venture(venture)


# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------


async def create_venture(venture: Venture):
    query = "INSERT INTO main.ventures(name, created_at ,phone_number, email, description, industries, funding_stage, website_url , funding_goal, total_funding, valuation, status) VALUES ($1, $2, $3, $4, $5, $6 ,$7 ,$8 ,$9 ,$10, $11, $12) RETURNING *"

    async with database.pool.acquire() as connection:
        elefanti_roz = await connection.fetchrow(query,
                                                 venture.name,
                                                 venture.created_at,
                                                 venture.phone_number,
                                                 venture.email,
                                                 venture.description,
                                                 venture.industries,
                                                 venture.funding_stage,
                                                 venture.website_url,
                                                 venture.funding_goal,
                                                 venture.total_funding,
                                                 venture.valuation,
                                                 venture.status)

        return elefanti_roz


@router.post("/")
async def post(venture: Venture):
    return await create_venture(venture)


# -----------------------------------------------------------------------------

async def get_venture_id(id: int):
    query = "SELECT * FROM main.ventures WHERE id = $1"

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id)

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Could not find venture with id={id} "
        )

    venture = Venture(
        name=row["name"],
        created_at=row["created_at"],
        phone_number=row["phone_number"],
        email=row["email"],
        description=row["description"],
        industries=row["industries"],
        funding_stage=row["funding_stage"],
        website_url=row["website_url"],
        funding_goal=row["funding_goal"],
        total_funding=row["total_funding"],
        valuation=row["valuation"],
        status=row["status"]
    )

    return {
        "id": row["id"],
        **venture.model_dump()
    }


@router.get("/{id}")
async def get_id(id: int):
    return await get_venture_id(id)


# -----------------------------------------------------------------------------

async def get_venture_id_members(id: int, limit: int, offset: int):
    query = '''
      SELECT u.user_id, u.name, u.role, u.email, u.gender, v.valuation
      FROM main.venture_members vm 
      JOIN main.users u
        ON u.user_id = vm.member_id 
      JOIN main.ventures v
        ON v.id = vm.venture_id 
      WHERE vm.venture_id = $1
      LIMIT $2 OFFSET $3
      '''

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, id, limit, offset)

        users = []

        for record in rows:
            user = User(
                name=record["name"],
                email=record["email"],
                role=record["role"],
                gender=record["gender"],
                password="placeholder"
            )

            users.append({
                **user.model_dump(),
                "user_id": record["user_id"],
                "valuation": record["valuation"]
            })

        return users


@router.get("/{id}/members")
async def get_id_members(id: int, limit: int = 10, offset: int = 0):
    return await get_venture_id_members(id, limit, offset)

# -----------------------------------------------------------------------------


async def delete_venture(id: int):
    query = "DELETE FROM main.ventures WHERE id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, id)

        return {
            "message": f"Venture with id {id} deleted successfully"
        }


@router.delete("/{id}")
async def delete(id: int):
    return await delete_venture(id)

# --------------------------------------------------


async def update_venture(id: int, venture: Venture):
    query = "UPDATE main.ventures SET name= $2, created_at=$3,  phone_number= $4, email= $5, description=$6, industries=$7, funding_stage=$8, website_url= $9, funding_goal=$10, total_funding=$11, valuation=$12, status=$13 WHERE id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, venture.name, venture.created_at,
                                 venture.phone_number,
                                 venture.email,
                                 venture.description,
                                 venture.industries,
                                 venture.funding_stage,
                                 venture.website_url,
                                 venture.funding_goal,
                                 venture.total_funding,
                                 venture.valuation,
                                 venture.status)

        return {
            "message": "Venture updated successfully",
            "venture": {"id": venture.id, **venture.model_dump()}
        }


@router.put("/{id}")
async def update(id: int, venture: Venture):
    return await update_venture(id, venture)
