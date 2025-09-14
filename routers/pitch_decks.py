from fastapi import APIRouter, HTTPException
from ..backend.model import PitchDecks
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
async def get_pitch_decks(limit: int, offset: int):
    query = "SELECT * FROM main.pitch_decks LIMIT $1 OFFSET $2"

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
    


@router.get("/{id}", response_model=PitchDecks)
async def get_pitch_deck_id(id: int, pitch_deck : PitchDecks):
    query = "SELECT *FROM main.pitch_decks WHERE id= $1"
    
    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id)
        
    if row is None:
        raise HTTPException(status_code=404, detail=f"Could not find pitch_deck with id={id}") 
    # could not find deck with id = 1 - nderkohe i kam ber post dhe get me t njejten id
    

    return PitchDecks(
        		deck_id=row["deck_id"],
                title=row["title"],
                file_url=row["file_url"],
                description=row["description"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
	)





        
	
    
@router.delete("/")
async def delete_pitch_deck(pitch: PitchDecks):
    query = "DELETE FROM main.pitch_decks WHERE (deck_id = $1  AND title = $2 AND file_url = $3 AND description = $4 AND created_at = $5 AND updated_at = $6 )"

    async with database.pool.acquire() as connection:
        await connection.execute(query,pitch.deck_id, pitch.title, pitch.file_url, pitch.description, pitch.created_at, pitch.updated_at)


@router.put("/{id}", response_model=PitchDecks)
async def update_pitch_deck(id: int, pitch_deck: PitchDecks):
    query = """
    UPDATE main.pitch_decks
    SET 
        deck_id = $2,
        title = $3,
        file_url = $4,
        description = $5,
        created_at = $6,
        updated_at = $7
    WHERE id = $1
    RETURNING *
    """

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(
            query,
            id,
            pitch_deck.deck_id,
            pitch_deck.title,
            pitch_deck.file_url,
            pitch_deck.description,
            pitch_deck.created_at,
            pitch_deck.updated_at
        )

    if row is None:
        raise HTTPException(status_code=404, detail=f"Pitch deck with id {id} does not exist")

    return PitchDecks(
        deck_id=row["deck_id"],
        title=row["title"],
        file_url=row["file_url"],
        description=row["description"],
        created_at=row["created_at"],
        updated_at=row["updated_at"]
    )

    
	
    


