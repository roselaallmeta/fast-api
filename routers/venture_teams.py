from enum import Enum
from multiprocessing import connection
from multiprocessing.managers import BaseManager
from fastapi import APIRouter, Depends, HTTPException, Query
from ..model import GenderEnum, User, UserRoleEnum, VentureTeam
from ..src.commons.postgres import database
from typing import List, Optional
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator


router = APIRouter(
    prefix="/venture_teams", responses={404: {"description": "Not found"}})



# "venture_teams": """
#         CREATE TABLE IF NOT EXISTS main.venture_teams (
#             venture_id INT NOT NULL REFERENCES main.ventures(id) ON DELETE CASCADE,
#             team_id INT NOT NULL REFERENCES main.teams(id) ON DELETE CASCADE,
#             created_at TIMESTAMP DEFAULT NOW(),
#             PRIMARY KEY (venture_id, team_id)
#         );
#     """,
# -----------------------------------------

async def get_all_ventureTeams(limit: int, offset: int) -> List:
	query = "SELECT * FROM main.venture_teams LIMIT $1 OFFSET $2"

	async with database.pool.acquire() as connection:
		rows = await connection.fetch(query, limit, offset)

		venture_teams = []

		for record in rows:
			venture_team = VentureTeam(
				id=record["id"],
				venture_id=record["venture_id"],
				team_id=record["team_id"],
				title=record["title"],
				created_at=record["created_at"]
			)

			venture_teams.append(venture_team)

		return venture_teams


@router.get("/")
async def get(limit: int = 10, offset: int = 0):
	return get_all_ventureTeams(limit, offset)


# -----------------------------------------------

async def get_ventureTeam_id(id: int):
			query = "SELECT * FROM main.venture_team WHERE id = $1"

			async with database.pool.acquire() as connection:
				row = await connection.fetchrow(query, id)


			if row is None:
				raise HTTPException(
          status_code=404, detail=f"Could not find team venture with id={id}")
	
			venture_team = VentureTeam(
					id=row["id"],
					venture_id=row["venture_id"],
					team_id=row["team_id"],
					title=row["title"],
					created_at=row["created_at"]
			)


			return {
					**venture_team.model_dump()
			}


@router.get("/{id}", response_model=VentureTeam)
async def get_ventureTeam_id(id: int):
		return await get_ventureTeam_id(id)
	

#-----------------------------------------


async def create_ventureTeam(ventureTeam: VentureTeam):
		query= "INSERT INTO main.venture_team (venture_id, team_id, created_at) RETURNING id, venture_id, team_id, title ,created_at "


		async with database.pool.acquire() as connection:
			row = await connection.fetchrow(query, ventureTeam.venture_id, ventureTeam.team_id, ventureTeam.title, ventureTeam.created_at)

			return row
		

@router.post("/")
async def create(ventureTeam : VentureTeam):
		return await create_ventureTeam(ventureTeam)
	
#------------------------------------------------------

async def delete_ventureTeam(id: int):
		query = "DELETE * FROM main. venture_team WHERE id = $1"

		async with database.pool.acquire() as connection:
			await connection.execute(query, id)

		return f"Venture team with id={id} has been deleted sucessfully."

@router.delete("/{id}")
async def delete(id: int):
		return await delete_ventureTeam(id)


#----------------------------------------------------------

async def update_ventureTeam(id: int, ventureTeam: VentureTeam):
		query = "UPDATE main.venture_team SET venture_id = $2, team_id = $3, title = $4, created_at = $5"

async def update_user(id: int, ventureTeam: VentureTeam):
    query = "UPDATE main.venture_team SET venture_id = $2, team_id = $3, title = $4 ,created_at = $5"

    async with database.pool.acquire() as connection:
        await connection.execute(query, ventureTeam.venture_id, ventureTeam.team_id,ventureTeam.title ,ventureTeam.created_at)

        return {
            "message": "User updated sucessfully",
            "user": {"id": id, **ventureTeam.model_dump()}
        }


@router.put("/{id}")
async def put(id: int, ventureTeam: VentureTeam):
    return await update_user(id, ventureTeam)








#-------------------------------------------------




	

	  
	
	
		
		
		

	






