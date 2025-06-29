from typing import List
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, File, UploadFile
from ..model import Document, Investment
from datetime import date, timedelta
from ..database import get_connection



router = APIRouter(
    prefix= "/",
    responses={404: {"description": "Not found"}}
)




async def insert_document(document: Document):
    query = "INSERT INTO main.document (user_id, title, size, issue_date, expiry_date, content_type, uploaded_by, description, status) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)"
    

    async with database.pool.acquire() as connection:
        await connection.execute(query, document.user_id,document.title, document.size, document.issue_date, document.expiry_date, document.content_type, document.uploaded_by, document.description, document.status)
        

        
async def update_document_by_id(id: int, updated : Document) -> Document | None:
    query =  """UPDATE main.document SET 
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
        row = await connection.fetchrow(query, updated.title, updated.size, updated.issue_date, updated.expiry_date, updated.content_type, updated.uploaded_by, updated.uploaded_at, updated.description, updated.status , id)
        if row:
            return Document(dict(row))
                
        return None
    


async def delete_document_by_id(id: int | None) -> str |None:
    query = "DELETE FROM main.document WHERE id = $1"
    
    async with database.pool.acquire() as connection:
        result = await connection.execute(query, id)

        
        if result.startswith("DELETE 1"):
            return "Document deleted successfully."

        return None
    


async def get_document_by_id(id : int | None) -> Document | None:
    query = "SELECT * FROM main.document WHERE id = $1"
    
    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id)
        
        if row:
            return Document(dict(row))
        
        return None
    


async def get_all_documents() -> List[Document]:
    query = """
SELECT
        title, 
        size, 
        issue_date, 
        expiry_date, 
        content_type, 
        uploaded_by, 
        uploaded_at, 
        description, 
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

        ) for record in rows
    ]
    return documents
    


    
    



            


              
        

    
				
        
		
        