from typing import List
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, File, UploadFile
from ..model import Team
from datetime import date, timedelta
from app.routers import teams
from enum import Enum
from multiprocessing import connection
from fastapi import APIRouter, HTTPException, Query
from ..src.commons.postgres import database
from typing import List, Optional
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# class Team(BaseModel):  # inseroje ne db
#     number_of_members: int
#     names: str
#     roles: str
#     startup_before: bool



router = APIRouter(prefix="/teams", responses={404: {"description": "Not found"}})


#------------------------------------------------------

async def get_team_id(team_id: int):
	query = "SELECT * FROM main.teams WHERE id = $1"

	async with database.pool.acquire() as connection:
		row = await connection.fetch(query, team_id)

	if row is None:
		raise HTTPException(
            status_code=404, detail=f"Could not find team with id={team_id}")
	

	team = Team(
		number_of_members= "number_of_members",
		names= "names",
		roles=row["roles"],
		startup_before=row["startup_before"]
	)
	
	return {
		"team_id" : row["id"],
		**team.model_dump()
	}


@router.get("/{id}", response_model=Team)
async def get_id(team_id: int):
	return await get_team_id(team_id)
#---------------------------------------------------------


async def get_teams(limit: int, offset: int) -> List:
	query = "SELECT * FROM main.teams LIMIT $1 OFFSET $2"

	async with database.pool.acquire() as connection:
		rows= await connection.fetch(query, limit, offset)

		teams = []
		for record in rows:

			team = Team(
				names=record["names"],
				number_of_members= record["number_of_members"],
				roles=record["roles"],
				startup_before=record["startup_before"]
			)

			teams.append({
				**team.model_dump(),
				"id": record["id"]
			})

		return teams
	

@router.get("/")
async def get_all_teams(limit: int = 10, offset: int = 0):
	return await get_teams(limit, offset)


#-----------------------------------------------------------

async def create_team(team: Team):
	query = "INSERT INTO main.teams (number_of_members, names, roles, startup_before) VALUES ($1, $2, $3, $4)"

	async with database.pool.acquire() as connection:
		await connection.execute(query, team.number_of_members, team.names, team.roles, team.startup_before)

		return {**team.model_dump()}
	


@router.post("/")
async def create(team: Team):
	return await create_team(team)

#----------------------------------------------------------------

async def update_team(id: int, team: Team):
	query = "UPDATE main.teams SET number_of_members = $2, names = $3, roles=$4, startup_before=$5 WHERE id=$1"

	async with database.pool.acquire() as connection:
		await connection.execute(query, id, team.number_of_members, team.names, team.roles, team.startup_before)


		return {
            "message": "Team updated successfully",
            "user": {"id": id, **team.model_dump()}
    }
	

@router.put("/{id}")
async def update_team_id(id: int, team: Team):
	return await update_team(id, team)

#------------------------------------------------------------------

async def delete_team(id:int):
	query = "DELETE FROM main.teams WHERE id = $1"

	async with database.pool.acquire() as connection:
		await connection.execute(query, id)

	return f"Team with id {id} deleted"

@router.delete("/{id}")
async def delete(id: int):
	return await delete_team(id)


