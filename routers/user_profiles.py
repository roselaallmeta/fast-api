from typing import List
from fastapi import APIRouter, HTTPException
from ..backend.model import UserProfile
from ..src.commons.postgres import database



router = APIRouter(
    prefix= "/user_profiles",
    responses={404: {"description": "Not found"}}
)


@router.post("/")
async def insert_user_profile(user_profiles: UserProfile):
    query = """INSERT INTO main.user_profiles(

    user_id,
    phone_number,
    created_at,
    updated_at,
    last_login,
    is_active,
    description) VALUES ($1, $2, $3, $4, $5, $6, $7 )"""

    async with database.pool.acquire() as connection:
        await connection.execute(
            query,
            user_profiles.user_id,
            user_profiles.phone_number,
            user_profiles.created_at,
            user_profiles.updated_at,
            user_profiles.last_login,
            user_profiles.is_active,
            user_profiles.description
            
        )
        




@router.put("/{id}", response_model=UserProfile)
async def update_user_profile(id: int, user_profile: UserProfile):
    query = """
    UPDATE main.user_profiles 
    SET user_id = $2, phone_number = $3, created_at = $4, updated_at = $5,
        last_login = $6, is_active = $7, description = $8
    WHERE id = $1 RETURNING *
    """

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(
            query,
            id, 
            user_profile.user_id,
            user_profile.phone_number,
            user_profile.created_at,
            user_profile.updated_at,
            user_profile.last_login,
            user_profile.is_active,
            user_profile.description
        )

    if row is None:
        raise HTTPException(status_code=404, detail=f"Profile with id {id} does not exist")

    return UserProfile(
        id=row["id"],
        user_id=row["user_id"],
        phone_number=row["phone_number"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        last_login=row["last_login"],
        is_active=row["is_active"],
        description=row["description"]
    )

    






    

@router.get("/")
async def get_user_profiles(limit: int, offset: int) -> List[UserProfile]:
    query = """
SELECT
        user_id,
        phone_number,
        created_at,
        updated_at,
        last_login,
        is_active,
        description 
        

FROM main.user_profiles
"""

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query)
    profiles = [
        UserProfile(
            user_id=record["user_id"],
            phone_number=record["phone_number"],
            created_at=record["created_at"],
            updated_at=record["updated_at"],
            last_login=record["last_login"],
            is_active=record["is_active"],
            description=record["description"]
            
        )
        for record in rows
    ]
    return profiles






@router.delete("/")
async def delete_user_profiles(profile: UserProfile):
    query = "DELETE FROM main.user_profiles WHERE (user_id = $1 AND phone_number = $2 AND created_at = $3 AND updated_at = $4 AND last_login = $5 AND is_active = $6 AND description = $7)"

    async with database.pool.acquire() as connection:
        await connection.execute(query, profile.user_id, profile.phone_number, profile.created_at, profile.updated_at, profile.last_login, profile.is_active, profile.description)
    

	

