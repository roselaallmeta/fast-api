from fastapi import APIRouter
from ..model import PitchDecks, User 
from ..src.commons.postgres import database
from typing import List, Optional


router = APIRouter(
    prefix= "/pitch_decks",
    responses={404: {"description": "Not found"}}
)




async def get_all_pitch_decks(limit: int, offset: int) -> List[PitchDecks]:
    query = "SELECT title, deck_id, file_url, description, created_at, updated_at FROM main.pitch_decks LIMIT $1 OFFSET $2"
    
    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)
        pitch_decks =  [PitchDecks(title=record["title"], deck_id =record['deck_id'],file_url=record['file_url'], description=record['description'], created_at=record['created_at']), updated_at=record['updated_at'] for record in rows]
        
        return pitch_decks



async def get_deck_by_venture_title(title: PitchDecks):
    query = """
SELECT 
    id,
    title,
    file_url,
    description,
    created_at,
    updated_at
FROM main.pitch_decks
WHERE title = $1
""" 
 
    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, main.pitch_decks(title))
        deck = [
    PitchDecks(
        id=record["id"],
        title=record["title"],
        file_url=record["file_url"],
        description=record["description"],
        created_at=record["created_at"],
        updated_at=record["updated_at"]
    )
    for record in rows
]
        return deck
    


async def get_deck_by_id(id: int | None) -> str | None:
    query = """
SELECT 
    *
FROM main.pitch_decks
WHERE id = $1
""" 

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, main.pitch_decks(id))
        deck = [
    PitchDecks(
        id=record["id"],
        title=record["title"],
        file_url=record["file_url"],
        description=record["description"],
        created_at=record["created_at"],
        updated_at=record["updated_at"]
    )
    for record in rows
]
        return deck



async def insert_pitch_deck(pitch_deck: PitchDecks) -> PitchDecks:
    query = """INSERT INTO main.pitch_decks (title, file_url, description, created_at, updated_at) VALUES ($1, $2, $3, $4, $5) WHERE id = $6
          RETURNING id, title, file_url, description, created_at, updated_at """
    

    async with database.pool.acquire() as connection:
        row = await connection.execute(query, pitch_deck.title, pitch_deck.file_url, pitch_deck.description, pitch_deck.created_at, pitch_deck.updated_at)
        
        return row
        
				
        
				

    