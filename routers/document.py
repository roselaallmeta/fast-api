from fastapi import APIRouter
from fastapi import HTTPException
from ..model import Document
from ..src.commons.postgres import database


router = APIRouter(prefix="/documents",
                   responses={404: {"description": "Not found"}})

# -------------------------------------------------------------------------


async def get_document_id(id: int):
    query = "SELECT document.user_id , document.title, document.add_document, document.issue_date, document.expiry_date, document.content_type,document.uploaded_by, document.description, document.uploaded_at, document.status FROM main.document WHERE id = $1"

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, id)

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Could not find document with id={id: int}")

    document = Document(
        user_id=row["user_id"],
        title=row["title"],
        add_document=row["add_document"],
        issue_date=row["issue_date"],
        expiry_date=row["expiry_date"],
        content_type=row["content_type"],
        uploaded_by=row["uploaded_by"],
        description=row["description"],
        uploaded_at=row["uploaded_at"],
        status=row["status"]
    )

    return {
        "document_id": row["id"],
        **document.model_dump()
    }


@router.get("/{id}", response_model=Document)
async def get_doc(id: int):
    return await get_document_id(id)

# --------------------------------------------------------------


async def get_all_docs(limit: int, offset: int):
    query = "SELECT * FROM main.document LIMIT $1 OFFSET $2"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, limit, offset)
        documents = []

        for record in rows:
            document = Document(
                user_id=record["user_id"],
                title=record["title"],
                add_document=record["add_document"],
                issue_date=record["issue_date"],
                expiry_date=record["expiry_date"],
                content_type=record["content_type"],
                uploaded_by=record["uploaded_by"],
                description=record["description"],
                uploaded_at=record["uploaded_at"],
                status=record["status"]
            )

            documents.append({
                **document.model_dump(),
                "id": record["id"]
            })

        return documents


@router.get("/")
async def get_documents(limit: int = 10, offset: int = 0):
    return await get_all_docs(limit, offset)

# ----------------------------------------------------------


async def upload_document(document: Document):
    query = "INSERT INTO main.document (user_id , title, add_document, issue_date, expiry_date, content_type, uploaded_by, description, uploaded_at, status) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) RETURNING *"

    async with database.pool.acquire() as connection:
        await connection.fetchrow(query, document.user_id, document.title, document.add_document, document.issue_date, document.expiry_date, document.content_type, document.uploaded_by, document.description, document.uploaded_at, document.status)

        return {**document.model_dump()}


@router.post("/")
async def create_document(document: Document):
    return await upload_document(document)

# -------------------------------------------------------------------


async def delete_document(id: int):
    query = "DELETE FROM main.document WHERE id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query, id)

    return f"Document with id {id} has been deleted sucessfully."


@router.delete("/{id}")
async def delete_doc(id: int):
    return await delete_document(id)


# -------------------------------------------------------

async def update_document(id: int, document: Document):
    query = "UPDATE main.document SET user_id=$2, title = $3, add_document = $4 ,issue_date = $5, expiry_date = $6, content_type = $7,      uploaded_by = $8 ,description = $9, uploaded_at=$10, status = $11 WHERE id = $1"

    async with database.pool.acquire() as connection:
        await connection.execute(query,

                                 document.user_id,
                                 document.title,
                                 document.add_document,
                                 document.issue_date,
                                 document.expiry_date,
                                 document.content_type,
                                 document.uploaded_by,
                                 document.description,
                                 document.uploaded_at,
                                 document.status
                                
                                 )

    return {
        "message": "Document updated sucessfully",
        "document": {"id": id, **document.model_dump()}
    }


@router.put("/{id}")
async def update_doc(id: int, document: Document):
    return await update_document(id, document)

# -----------------------------------------------------------------------


