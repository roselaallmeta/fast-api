from typing import List
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, File, UploadFile
from ..model import Team, TeamMembers
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

# tek teams
# ky useri tek cili team eshte member
# from team members tm select ktot t dhenat me join


async def get_team_id(id: int):
    query = "SELECT * FROM main.teams WHERE id = $1"

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id)

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Could not find team with id={id}")

    team = Team(
        id="id",
        name="name",
        created_at="created_at"
    )

    return {
        "id": row["id"],
        **team.model_dump()
    }


@router.get("/{id}/", response_model=Team)
async def get_id(id: int):
    return await get_team_id(id)

# ---------------------------------------------------------


async def get_teams(limit: int, offset: int) -> List:
    query = "SELECT * FROM main.teams LIMIT $1 OFFSET $2"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)

        print("-----------------------------------------------------")
        print("-----------------------------------------------------")
        print(rows)
        print("-----------------------------------------------------")
        print("-----------------------------------------------------")

        teams = []

        for record in rows:
            team = Team(

                id=record["id"],
                name=record["name"],
                created_at=record["created_at"]

            )

            

            teams.append({
                **team.model_dump(),
                "id": record["id"]
            })

        return teams


@router.get("/")
async def get_all_teams(limit: int = 10, offset: int = 0):
    return await get_teams(limit, offset)


# -----------------------------------------------------------
# krijon nje team - merr id te team qe ke krijuar - insert nje new team member
# links each member to that team


# list me id te userave qe do ti bej members tek team
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

        for id in members:  # id e nje useri qe do t besh member
            # i jep id e team dhe id te userit qe do rregjistorhet si member
            new_member = await connection.fetch(tm_query, new_team["id"], id)
            # per secilen id te lista- insert id e team dhe id e userit qe do behet member

            inserted_members.append(new_member)
            
        return {
          "team": new_team,
          "members": inserted_members
        }


@router.post("/")
async def create(team: Team, members: List[int]):
    return await create_team(team, members)


# async def create_team(team: Team, members : List[str]):
#     query = "INSERT INTO main.teams (name) VALUES ($1) RETURNING id"

#     async with database.pool.acquire() as connection:
#         team_rows = await connection.fetch(query)

#         team_id=team_rows[0]["id"];

#         for member_id in members:
#             tm_query = "INSERT INTO main.team_members (team_id, member_id) VALUES ($1, $2)"
#             inserted_member = await connection.execute(tm_query, team_id, member_id)


#         inserted_members = []

#         for member_id in members:
#             inserted_members.append(member_id)

#     return inserted_members


# @router.post("/")
# async def create(team: Team, members: List[str]):
#     return await create_team(team, members)


# ----------------------------------------------------------------

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
# te vijn members te ktij team


# /teams/id/members


# endpoint that lists all teams a user belongs to

async def list_user_teams(team: Team, id: int):
    query = "SELECT u.id, tm.member_id, tm.team_id FROM main.users u INNER JOIN main.team_members tm ON u.id = tm.id WHERE u.id = $1"

    async with database.pool.acquire() as connection:
        joined_row = await connection.fetch(query)


# async def list_user_teams(id: int, member: TeamMembers):

#     query = "SELECT users.id , team_members.member_id, team_members.team_id FROM main.users INNER JOIN main.team_members ON users.id = team_members.member_id WHERE users.id = $1"

#     async with database.pool.acquire() as connection:
#        rows = await connection.fetch(query, id, member)

#        user_teams = []

#        for record in rows:
#             user_team = TeamMembers(
#                 team_id = record["team_id"],
#                 member_id=record["member_id"],
#                 created_at=record["created_at"]
# 						)

#             user_teams.append(user_team)

#        return user_teams


# @router.get("/{id}/members")
# async def list_teams(id: int, member: TeamMembers):
#     return await list_user_teams(id, member)


# ----------------------------------------------------


# mos merr dhe id e team dhe te member

# teams/id/members - nuk behet endpoint i ri per kte entitetin qe po krijon

# @router.get("/{id}/{member_id}")
# async def get_all_teams_of_member(id:int, member_id:int):
#     return await list_user_teams(id, member_id)
