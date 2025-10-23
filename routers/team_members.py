from typing import List
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, File, UploadFile
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
    prefix="/team_members", responses={404: {"description": "Not found"}})


#---------------------------------------------------------------

async def get_team_members(limit: int, offset: int):
    query = "SELECT * FROM main.team_members LIMIT $1 OFFSET $2"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query , limit, offset)
        
        team_members = []
        
        for record in rows:
            team_member = TeamMembers (
                team_id=record["team_id"],
                member_id=record["member_id"],
                created_at=record["created_at"]
						   )
            
            team_members.append(team_member)
        
        return team_members
    
		
@router.get("/")
async def get(limit: int, offset: int):
    return await get_team_members(limit, offset)
                 

# ------------------------------------------------------

async def create_team_members(team_members: TeamMembers):
    query = "INSERT INTO main.team_members (team_id, member_id, created_at) VALUES ($1, $2, $3) RETURNING *"
    
    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, team_members.team_id, team_members.member_id, team_members.created_at)
        
        return row



@router.post("/")
async def post(team_members: TeamMembers):
    return await create_team_members(team_members)



#----------------------------------------------------------


async def delete_team_member(team_id: int, member_id: int):
    query = "DELETE FROM main.team_members WHERE (team_id, member_id) = ($1 ,$2)"
    
    async with database.pool.acquire() as connection:
        await connection.execute(query, team_id, member_id)
        
    return f"Member with member ID {member_id} that belongs to team with id s=  {team_id} has been deleted sucessfully."
         
@router.delete("/{team_id}/{member_id}")
async def delete(team_id: int, member_id: int):
    return await delete_team_member(team_id, member_id)
    

#-------------------------------------

# function qe e fshin nje member nga nje team

async def leave_team(team_id: int, member_id: int):
    query = "DELETE FROM main.team_members WHERE team_id = $1 AND member_id = $2"
    
    async with database.pool.acquire() as connection:
        leaveTeam_rows = await connection.execute(query, team_id, member_id)
        
        print("----------------------------------")
        print(leaveTeam_rows)
        
        return "Member deleted sucessfully"; 
        


@router.delete("/leave-team/{team_id}/{member_id}")
async def delete(team_id: int, member_id: int):
    return await leave_team(team_id, member_id) 
        


         
    
		
    
    















#2- function that checks nese nje member belongs to a specific team