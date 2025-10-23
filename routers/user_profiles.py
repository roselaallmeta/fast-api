from typing import List
from fastapi import APIRouter, HTTPException
from ..model import UserProfile
from ..src.commons.postgres import database


router = APIRouter(
    prefix="/user_profiles",
    responses={404: {"description": "Not found"}}
)
# -----------------------------------------------------------------------------------


async def insert_user_profile(user_profile: UserProfile):
    query = """INSERT INTO main.user_profiles(
    user_id,
    gender,
    phone_number,
    created_at,
    updated_at,
    status,
    industry,
    description) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING * """

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(
            query,
            user_profile.user_id,
            user_profile.gender,
            user_profile.phone_number,
            user_profile.created_at,
            user_profile.updated_at,
            user_profile.status,
            user_profile.industry,
            user_profile.description
        )

        return row


@router.post("/")
async def post(user_profile: UserProfile):
    return await insert_user_profile(user_profile)


# -----------------------------------------------------------------------------------



async def update_user_profile(id: int, user_profile: UserProfile):
    query = """
    UPDATE main.user_profiles
    SET user_id = $2, gender = $3, phone_number = $4, created_at = $5, updated_at = $6, status = $7, industry = $8, description = $9
    WHERE id = $1 RETURNING *
    """

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(
            query,
            id,
            user_profile.user_id,
            user_profile.gender,
            user_profile.phone_number,
            user_profile.created_at,
            user_profile.updated_at,
            user_profile.status,
            user_profile.industry,
            user_profile.description
        )

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Profile with id {id} does not exist")

    return UserProfile(
        id=row["id"],
        user_id=row["user_id"],
        gender=row["gender"],
        phone_number=row["phone_number"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        status=row["status"],
        industry=row["industry"],
        description=row["description"]
    )


@router.put("/{id}", response_model=UserProfile)
async def put(id: int, user_profile: UserProfile):
    return await update_user_profile(id, user_profile)


# -----------------------------------------------------------------------------------


@router.get("/")
async def get_user_profiles(limit: int, offset: int) -> List:
    query = """
      SELECT
        id,
        user_id,
        gender,
        phone_number,
        created_at,
        updated_at,
        status,
        industry,
        description

    FROM main.user_profiles LIMIT $1 OFFSET $2
  """

    profiles = []

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)

        for record in rows:
            profile = UserProfile(
                id=record["id"],
                user_id=record["user_id"],
                gender=record['gender'],
                phone_number=record["phone_number"],
                created_at=record["created_at"],
                updated_at=record["updated_at"],
                status=record["status"],
                industry=record["industry"],
                description=record["description"]
            )

            profiles.append(profile)

        return profiles


@router.get("/")
async def get(limit: int = 10, offset: int = 0):
    return await get_user_profiles(limit, offset)


# -----------------------------------------------------------------------------------


async def delete_user_profiles(id: int):
    query = "DELETE FROM main.user_profiles WHERE id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, id)

    return f"User with ID {id} has been deleted sucessfully."


@router.delete("/{id}")
async def delete(id: int):
    return await delete_user_profiles(id)
