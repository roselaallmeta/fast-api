from fastapi import APIRouter
from ..model import PitchDecks
from typing import List
from ..src.commons.postgres import database

router = APIRouter(prefix="/pitch_decks", responses={404: {"description": "Not found"}})


@router.post("/")
async def insert_pitch_deck(pitch_deck: PitchDecks):
    query = """
    INSERT INTO main.pitch_decks (
		deck_id,
        title,
        file_url,
        description,
        created_at,
        updated_at
    ) VALUES (
        $1, $2, $3, $4, $5, $6
    )RETURNING id
"""

    async with database.pool.acquire() as connection:
        await connection.execute(
            query,
            pitch_deck.deck_id,
            pitch_deck.title,
            pitch_deck.file_url,
            pitch_deck.description,
            pitch_deck.created_at,
            pitch_deck.updated_at
        )
        return {"message": "Pitch deck inserted"}



@router.get("/")
async def get_pitch_decks(limit: int, offset: int) -> List[PitchDecks]:
    query = "SELECT deck_id, title, file_url, description, created_at, updated_at FROM main.pitch_decks LIMIT $1 OFFSET $2"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)
        pitch_decks = [
            PitchDecks(
                
                deck_id=record["deck_id"],
                title=record["title"],
                file_url=record["file_url"],
                description=record["description"],
                created_at=record["created_at"],
                updated_at=record["updated_at"]
            )
            for record in rows
        ]

        return pitch_decks





@router.delete("/")
async def delete_pitch_deck(pitch: PitchDecks):
    query = "DELETE FROM main.pitch_decks WHERE (deck_id = $1  AND title = $2 AND file_url = $3 AND description = $4 AND created_at = $5 AND updated_at = $6 )"

    async with database.pool.acquire() as connection:
        await connection.execute(query,pitch.deck_id, pitch.title, pitch.file_url, pitch.description, pitch.created_at, pitch.updated_at)
