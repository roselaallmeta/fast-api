from fastapi import APIRouter
from ..model import VentureMembers
from ..src.commons.postgres import database
from typing import List, Optional


router = APIRouter(prefix="/venture_members", responses={404: {"description": "Not found"}})


@router.get("/")
async def get_venture_members(limit: int, offset: int) -> List[VentureMembers]:
    query = "SELECT venture_id, member_id,  name, email, position, gender FROM main.venture_members LIMIT $1 OFFSET $2"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)
        members = [
            VentureMembers(
                venture_id=record["venture_id"],
                member_id=record["member_id"],
                name=record["name"],
                email=record["email"],
                position=record["position"],
                gender=record["gender"]
            )
            for record in rows
        ]
        return members
    



@router.post("/")
async def insert_member(member: VentureMembers):
    query = "INSERT INTO main.venture_members (venture_id, member_id,  name, email, position, gender) VALUES ($1, $2, $3, $4, $5 , $6)"

    async with database.pool.acquire() as connection:
        await connection.execute(query, member.venture_id, member.member_id ,member.name, member.email, member.position, member.gender)
        


	


@router.delete("/")
async def delete_user(member: VentureMembers):
    query = "DELETE FROM main.venture_members WHERE (member_id = $1 AND name = $2 AND email = $3 AND position = $4 AND gender = $5)"

    async with database.pool.acquire() as connection:
        await connection.execute(query, member.member_id, member.name, member.email,member.position, member.gender)
