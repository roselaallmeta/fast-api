from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi import FastAPI, File, UploadFile
from fastapi.security import OAuth2PasswordBearer

from ..model import Team, TeamMembers, User
from datetime import date, timedelta
# from app.routers import teams
from enum import Enum
from multiprocessing import connection
from fastapi import APIRouter, HTTPException, Query
from ..src.commons.postgres import database
from typing import List, Optional
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


router = APIRouter(
    prefix="/teams", responses={404: {"description": "Not found"}})

# ------------------------------------------------------



async def get_team_id(id: int):
    query = "SELECT * FROM main.teams WHERE id = $1"

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id)

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Could not find team with id={id}")
    
    team = Team(
        name="name"
    )

    return {
        "id": row["id"],
        **team.model_dump()
    }


@router.get("/{id}/", response_model=Team)
async def get_id(id: int):
    return await get_team_id(id)

# ---------------------------------------------------------



async def get_teams(limit: int, offset: int, memberId: int) -> List:
    query = "SELECT * FROM main.teams LIMIT $1 OFFSET $2"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)

        print("-----------------------------------------------------")
        print("-----------------------------------------------------")
        print(rows)
        print("-----------------------------------------------------")
        print("-----------------------------------------------------")
        teams = []
        success = True

        for record in rows:
            if (memberId):
              
                members_query = "SELECT team_id, member_id FROM main.team_members WHERE team_id = $1 AND member_id = $2"
                memberId_defined = await connection.fetch(members_query)
                return memberId_defined

            team = Team(
                name=record["name"]
						)


            teams.append({
                **team.model_dump(),
                "id": record["id"],
            })
        return teams


@router.get("/?memberId")
async def get_all_teams(limit: int = 10, offset: int = 0, memberId=bool):
    return await get_teams(limit, offset, memberId)
# -----------------------------------------------------------

async def create_team(team: Team, members: List[int]):
    query = "INSERT INTO main.teams (name) VALUES ($1) RETURNING *"

    async with database.pool.acquire() as connection:
        team_rows = await connection.fetch(query, team.name)

        print("-------------------------------------------------")
        print(team_rows)
        print("-------------------------------------------------")
        new_team = team_rows[0]
        inserted_members = []

        tm_query = "INSERT INTO main.team_members (team_id, member_id) VALUES ($1, $2) RETURNING *"

        for id in members:  
            new_member = await connection.fetch(tm_query, new_team["id"], id)
            

            inserted_members.append(new_member)

        return {
            "team": new_team,
            "members": inserted_members
        }


@router.post("/")
async def create(team: Team, members: List[int]):
    return await create_team(team, members)

# ----------------------------------------------------------



async def delete_user_from_team(team_id: int, member_id: int):
    query = "SELECT * FROM main.team_members WHERE team_id = $1 AND member_id = $2"

    async with database.pool.acquire() as connection:
        selected_member = await connection.fetch(query, team_id, member_id)
        if not selected_member:
            return {"error": "User is not a member of this team."}

        if (selected_member):
            delete_query = "DELETE FROM main.team_members WHERE member_id = $2 AND team_id = $1"
            await connection.execute(delete_query, team_id, member_id)
        return f"User with ID {member_id} has been deleted sucessfully."


@router.delete("/{team_id}/leave-team/{member_id}")
async def leave_team(team_id: int, member_id: int):
    return await delete_user_from_team(team_id, member_id)
# -----------------------------------------------------------


async def join_team(team_id: int, member_id: int):
    query = "SELECT * FROM main.users WHERE id = $1"

    async with database.pool.acquire() as connection:
        selected_user = await connection.fetchrow(query, team_id, member_id)

        if (selected_user):
            new_query = "SELECT * FROM main.team_members WHERE team_id = $1 AND member_id = $2"
            existing_member = await connection.fetch(new_query, team_id, member_id)
            if not existing_member:
                insert_query = "INSERT INTO main.team_members (team_id, member_id) VALUES ($1, $2)"
                insert_member = await connection.fetch(insert_query, team_id, member_id)

            return insert_query


@router.post("/{team_id}/join/{id}")
async def user_join_team(team_id: int, id: int):
    return await join_team(team_id, id)


# -------------------------------
 
    

async def update_team(id: int, team: Team):
    query = "UPDATE main.teams SET name = $2 , created_at= $3 WHERE id=$1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, id, team.name, team.created_at)

        return {
            "message": "Team updated successfully",
            "user": {"id": id, **team.model_dump()}
        }


@router.put("/{id}")
async def update_team_id(id: int, team: Team):
    return await update_team(id, team)

# ------------------------------------------------------------------


async def delete_team(id: int):
    query = "DELETE FROM main.teams WHERE id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, id)

    return f"Team with id {id} deleted"


@router.delete("/{id}")
async def delete(id: int):
    return await delete_team(id)


# ----------------------------------------


async def list_user_teams(team: Team, id: int):
    query = "SELECT u.id, tm.member_id, tm.team_id FROM main.users u INNER JOIN main.team_members tm ON u.id = tm.id WHERE u.id = $1"

    async with database.pool.acquire() as connection:
        joined_row = await connection.fetch(query)
