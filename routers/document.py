from typing import List
from fastapi import APIRouter
from ..model import Document
from ..src.commons.postgres import database
router = APIRouter(prefix="/documents", responses={404: {"description": "Not found"}})



@router.get("/", response_model=List[Document])
async def get_all_documents(limit: int = 10, offset: int = 0):
    query = """
SELECT
		user_id,
        title, 
        size, 
        issue_date, 
        expiry_date, 
        content_type, 
        uploaded_by,  
        description, 
        uploaded_at,
        status

FROM main.document
"""

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query)
    documents = [
        Document(
            user_id=record["user_id"],
            title=record["title"],
            size=record["size"],
            issue_date=record["issue_date"],
            expiry_date=record["expiry_date"],
            content_type=record["content_type"],
            uploaded_by=record["uploaded_by"],
            uploaded_at=record["uploaded_at"],
            description=record["description"],
            status=record["status"]
        )
        for record in rows
    ]
    return documents



@router.post("/")
async def insert_document(document: Document):
    query = "INSERT INTO main.document (user_id, title, size, issue_date, expiry_date, content_type, uploaded_by,uploaded_at, description, status) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)"

    async with database.pool.acquire() as connection:
        await connection.execute(
            query,
            document.user_id,
            document.title,
            document.size,
            document.issue_date,
            document.expiry_date,
            document.content_type,
            document.uploaded_by,
            document.uploaded_at,
            document.description,
            document.status
        )
        


@router.delete("/")
async def delete_user(document: Document):
    query = "DELETE FROM main.document WHERE (user_id = $1 AND title = $2 AND size = $3 AND issue_date = $4 AND expiry_date = $5 AND content_type = $6 AND uploaded_by = $7 AND description = $8 AND uploaded_at = $9 AND status = $10)"

    async with database.pool.acquire() as connection:
        await connection.execute(
    query,
    document.user_id,
    document.title,
    document.size,
    document.issue_date,
    document.expiry_date,
    document.content_type,
    document.uploaded_by,
    document.description,
    document.uploaded_at,
    document.status
)








#----------------------------------

@router.put("/")
async def update_document_by_id(id: int, updated: Document) -> Document | None:
    query = """UPDATE main.document SET 
        title = $1, 
        size = $2, 
        issue_date = $3, 
        expiry_date = $4 , 
        content_type = $5, 
        uploaded_by = $6, 
        uploaded_at = $7, 
        description = $8, 
        status = $9
        
        WHERE id = $10
                    
        RETURNING id, title, size, issue_date, expiry_date, content_type, uploaded_by, uploaded_at, description, status"""

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(
            query,
            updated.title,
            updated.size,
            updated.issue_date,
            updated.expiry_date,
            updated.content_type,
            updated.uploaded_by,
            updated.uploaded_at,
            updated.description,
            updated.status,
            id,
        )
        if row:
            return Document(dict(row))

        return None





# @router.get("/{id}")
# async def get_document_by_id(id: int | None) -> Document | None:
#     query = "SELECT * FROM main.document WHERE id = $1"

#     async with database.pool.acquire() as connection:
#         row = await connection.fetchrow(query, id)

#         if row:
#             return Document(dict(row))

#         return None