from fastapi import APIRouter, HTTPException
from ..src.commons.postgres import database
from typing import List, Optional
from ..model import VentureMembers


router = APIRouter(prefix="/venture_members", responses={404: {"description": "Not found"}})


#---------------------------------



async def get_members(limit: int, offset: int)-> List:
	query = "SELECT * FROM main.venture_members LIMIT $1 OFFSET $2"


	async with database.pool.acquire() as connection:
		rows = await connection.fetch(query, limit , offset)

		venture_members = []

		for record in rows:
			member = VentureMembers(
				venture_id=record["venture_id"],
        member_id=record["member_id"],
        name=record["name"]
			)

			venture_members.append({
				**member.model_dump(),
				"id": record["id"]
			})


	return venture_members
	

@router.get("/")
async def get(limit: int = 0, offset: int = 10):
	return await get_members(limit, offset)

#---------------------------------------------

async def get_member_id(id: int):
	query = "SELECT * FROM main.venture_members WHERE id = $1"

	async with database.pool.acquire() as connection:
		row = await connection.fetchrow(query, id)

	if row is None:
		raise HTTPException(
            status_code=404, detail=f"Could not find member with id={id}")
	
	member = VentureMembers(
		    venture_id=row["venture_id"],
        member_id=row["member_id"],
        name=row["name"]
	)


	return {
		"id": row["id"],
		**member.model_dump()
	}


@router.get("/{id}")
async def get_id(id: int):
	return await get_member_id(id)


#--------------------------------------------------


async def post_member(member: VentureMembers):
	query = "INSERT INTO main.venture_members( venture_id, member_id, name) VALUES ( $1, $2, $3 )"

	async with database.pool.acquire() as connection:
		await connection.execute(query, member.venture_id, member.member_id, member.name )


		return {**member.model_dump()}


@router.post("/")
async def post(member: VentureMembers):
    return await post_member(member)


#-----------------------------------


async def update_member(id: int, member: VentureMembers):
	query = "UPDATE main.venture_members SET venture_id = $2, member_id=$3, name = $4 WHERE id = $1"

	async with database.pool.acquire() as connection:
		await connection.execute(query, id, member.venture_id, member.member_id, member.name)


		return {
            "message": "Member updated sucessfully",
            "user": {"id": id, **member.model_dump()}
    }
	

@router.put("/{id}")
async def update_team_id(id: int, member:VentureMembers):
	return await update_member(id, member)


#-----------------------------------------------------------

async def delete_member(id:int):
	query = "DELETE FROM main.venture_members WHERE id=$1"

	async with database.pool.acquire() as connection:
		await connection.execute(query, id)

	return f"Member with ID {id} has been deleted sucessfully."


@router.delete("/{id}")
async def delete(id: int):
    return await delete_member(id)


	





	

