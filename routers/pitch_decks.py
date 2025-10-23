from fastapi import APIRouter, HTTPException
from ..model import PitchDecks
from typing import List
from ..src.commons.postgres import database

router = APIRouter(prefix="/pitch_decks",
                   responses={404: {"description": "Not found"}})



async def create_pitch(pitch_deck: PitchDecks):
    query = "INSERT INTO main.pitch_decks ( venture_id ,title, file_url, description, created_at, updated_at) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *"

    async with database.pool.acquire() as connection:
        await connection.execute(query,pitch_deck.venture_id, pitch_deck.title, pitch_deck.file_url, pitch_deck.description, pitch_deck.created_at, pitch_deck.updated_at)

        return {**pitch_deck.model_dump()}


@router.post("/")
async def create(pitch_deck: PitchDecks):
    return await create_pitch(pitch_deck)

# -------------------------------------------------


async def get_pitch_id(id: int):
    query = "SELECT * FROM main.pitch_decks WHERE id=$1"

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id)

        if row is None:
            raise HTTPException(
                status_code=404, detail=f"Could not find pitch deck with id={id}")

        pitch_deck = PitchDecks(
            id=row["id"],
            venture_id=row["venture_id"],
            title=row["title"],
            file_url=row["file_url"],
            description=row["description"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    return {
        "id": row["id"],
        **pitch_deck.model_dump()
    }


@router.get("/{id}")
async def get_id(id: int):
    return await get_pitch_id(id)

# ---------------------------------------------------------


async def get_pitch(limit: int, offset: int) -> List:
    query = "SELECT * FROM main.pitch_decks LIMIT $1 OFFSET $2"

    pitch_decks = []

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)

        for row in rows:
            pitch_deck = PitchDecks(
                # id=row["id"],
                venture_id=row["venture_id"],
                title=row["title"],
                file_url=row["file_url"],
                description=row["description"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )

            pitch_decks.append({
                "id": row["id"],
                **pitch_deck.model_dump()
            })

        return pitch_decks


@router.get("/")
async def get(limit: int = 10, offset: int = 0):
    return await get_pitch(limit, offset)


# -----------------------------------------------------------


async def delete_pitch(id: int):
    query = "DELETE FROM main.pitch_decks WHERE id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, id)

    return f"Pitch deck with ID{id} deleted sucessfully."


@router.delete("/{id}")
async def delete(id: int):
    return await delete_pitch(id)


# ---------------------------------------------------------

async def update_pitch_deck(id: int, pitch_deck: PitchDecks):
    query = "UPDATE main.pitch_decks SET venture_id=$2, title=$3, file_url=$4, description =$5 ,created_at=$6, updated_at=$7 WHERE id=$1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, id,  pitch_deck.venture_id, pitch_deck.title, pitch_deck.file_url, pitch_deck.description, pitch_deck.created_at, pitch_deck.updated_at)

        return {
            "message": "Pitch deck updated sucessfully",
            "user": {"deck_id": pitch_deck.id, **pitch_deck.model_dump()}
        }


@router.put("/{id}")
async def update(id: int, pitch_deck: PitchDecks):
    return await update_pitch_deck(id, pitch_deck)

# --------------------------------------------------------------
