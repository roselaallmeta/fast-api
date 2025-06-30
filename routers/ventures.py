from fastapi import APIRouter, FastAPI, Query

from app.src.commons.postgres import DATABASE_URL
from ..model import Venture
from typing import Annotated, List
from app.routers import ventures
from app.db import database


# from app.db import get_connection


router = APIRouter(prefix="/ventures", responses={404: {"description": "Not found"}})


@router.post("/")
async def insert_venture(venture: Venture):
    query = """
    INSERT INTO main.ventures (
        name,
        created_at,
        phone_number,
        email,
        description,
        industries,
        funding_stage,
        founders_name,
        founder_email,
        website_url,
        funding_goal,
        total_funding,
        valuation,
        is_active
    ) VALUES (
        $1, $2, $3, $4, $5, $6, $7,
        $8, $9, $10, $11, $12, $13, $14
    )
"""

    async with database.pool.acquire() as connection:
        await connection.execute(
            query,
            venture.name,
            venture.created_at,
            venture.phone_number,
            venture.email,
            venture.description,
            venture.industries,
            venture.funding_stage,
            venture.founders_name,
            venture.founder_email,
            venture.website_url,
            venture.funding_goal,
            venture.total_funding,
            venture.valuation,
            venture.is_active,
        )


@router.get("/")
async def get_all_ventures(limit: int, offset: int) -> List[Venture]:
    query = "SELECT * FROM main.ventures"

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query)
        ventures = Venture(
            name=rows["name"],
            created_at=rows["created_at"],
            phone_number=rows["phone_number"],
            email=rows["email"],
            description=rows["description"],
            industries=rows["industries"],
            funding_stage=rows["funding_stage"],
            website_url=rows["website_url"],
            funding_goal=rows["funding_goal"],
            total_funding=rows["total_funding"],
            valuation=rows["valuation"],
            is_active=rows["is_active"],
        )
        return ventures


@router.get("/{name}")
async def get_venture_by_name(venture: Venture) -> Venture | None:
    query = """
        SELECT 
            name,
            created_at,
            phone_number,
            email,
            description,
            industries,
            funding_stage,
            website_url,
            funding_goal,
            total_funding,
            valuation,
            is_active
        FROM main.ventures
        WHERE name = $1
    """

    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, venture.name)
        if row:
            return Venture(
                name=row["name"],
                created_at=row["created_at"],
                phone_number=row["phone_number"],
                email=row["email"],
                description=row["description"],
                industries=row["industries"],
                funding_stage=row["funding_stage"],
                website_url=row["website_url"],
                funding_goal=row["funding_goal"],
                total_funding=row["total_funding"],
                valuation=row["valuation"],
                is_active=row["is_active"],
            )
        return None


@router.get("/{industry}")
async def get_venture_by_industy(venture: Venture) -> Venture | None:
    query = """
        SELECT 
            industries
        FROM main.ventures
        WHERE industries = $1
    """

    async with DATABASE_URL.pool.acquire() as connection:
        row = await connection.fetchrow(query, venture.industries)
        if row:
            return Venture(
                name=row["name"],
                created_at=row["created_at"],
                phone_number=row["phone_number"],
                email=row["email"],
                description=row["description"],
                industries=row["industries"],
                funding_stage=row["funding_stage"],
                website_url=row["website_url"],
                funding_goal=row["funding_goal"],
                total_funding=row["total_funding"],
                valuation=row["valuation"],
                is_active=row["is_active"],
            )
        return None


@router.get("/{id}")
async def get_venture_by_id(venture: Venture) -> Venture | None:
    query = """
        SELECT 
            id
        FROM main.ventures
        WHERE id = $1
    """

    async with DATABASE_URL.pool.acquire() as connection:
        row = await connection.fetchrow(query, venture.id)
        if row:
            return Venture(
                name=row["name"],
                created_at=row["created_at"],
                phone_number=row["phone_number"],
                email=row["email"],
                description=row["description"],
                industries=row["industries"],
                funding_stage=row["funding_stage"],
                website_url=row["website_url"],
                funding_goal=row["funding_goal"],
                total_funding=row["total_funding"],
                valuation=row["valuation"],
                is_active=row["is_active"],
            )
        return None


@router.delete("/")
async def delete_venture(venture: Venture):
    query = """
DELETE FROM main.ventures
WHERE name = $1
  AND created_at = $2
  AND phone_number = $3
  AND email = $4
  AND description = $5
  AND industries = $6
  AND funding_stage = $7
  AND website_url = $8
  AND funding_goal = $9
  AND total_funding = $10
  AND valuation = $11
  AND is_active = $12
  AND founders_name = $13
  AND founder_email = $14
"""

    async with database.pool.acquire() as connection:
        await connection.execute(
            query,
            venture.name,
            venture.created_at,
            venture.phone_number,
            venture.email,
            venture.description,
            venture.industries,
            venture.funding_stage,
            venture.founders_name,
            venture.founder_email,
            venture.website_url,
            venture.funding_goal,
            venture.total_funding,
            venture.valuation,
            venture.is_active,
        )


@router.delete("/{id}")
async def delete_ventures_by_id(id: int | None) -> str | None:
    query = "DELETE FROM main.ventures WHERE id = $1"

    async with database.pool.acquire() as connection:
        result = await connection.execute(query, id)

        if result.startswith("DELETE 1"):
            return "Venture deleted successfully."

        return None


# startups = []


# #creating  a valid startup in the database
# @router.post("/")
# async def create_startup(startup: StartUp):

#     try:
#         connection = get_connection()
#         cursor = connection.cursor()
#         cursor.execute("""
#                        INSERT INTO startups(id, name , created_at, invested_at , description, founders_name, email, website_url, total_funding, is_active)
#                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s , %s)
#                        """ (startup.id , startup.name , startup.created_at, startup.invested_at, startup.description, startup.founders_name, startup.email, startup.website_url, startup.total_funding, startup.is_active))

#         connection.commit()
#         cursor.close()
#         connection.close()

#         return {"message": "Startup successfully added"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# #retrieve the startup by name
# @router.get("/{name}")
# async def get_startup_name(
#     name: str
# ):

#     connection = get_connection()
#     cursor = connection.cursor()
#     query = "SELECT name FROM startups WHERE name = %s"

#     cursor.execute(query, (name,))

#     result = cursor.fetchone()

#     cursor.close()
#     connection.close()

#     if result:
#         return {"startup": result, "message": "Startup found"}
#     else:
#         raise HTTPException(status_code=404, detail="No startup with that name.")


# @router.get("/{id}")
# async def get_startup_id(
#     id: int
# ):

#     connection = get_connection()
#     cursor = connection.cursor()
#     query = "SELECT id FROM startups WHERE id = %s"

#     cursor.execute(query, (id,))

#     result = cursor.fetchone()

#     cursor.close()
#     connection.close()

#     if result:
#         return {"startup": result, "message": "Startup found"}
#     else:
#         raise HTTPException(status_code=404, detail="No startup with that id.")


# # te marr nje startup ta marresh  nga emri i founderit
# @router.get("/{founders_name}")
# async def get_founder_name(
#     founders_name: str
# ):

#     connection = get_connection()
#     cursor = connection.cursor()
#     query = "SELECT founders_name FROM startups WHERE founders_name = %s"

#     cursor.execute(query, (founders_name,))

#     result = cursor.fetchone()

#     cursor.close()
#     connection.close()

#     if result:
#         return {"founders_name": result, "message": "Startup found by founders name."}
#     else:
#         raise HTTPException(status_code=404, detail="No startup found.")


# #get all startups as a list
# @router.get("/")
# async def get_startup():

#     connection = get_connection()
#     cursor = connection.cursor()
#     query = "SELECT * FROM startups"

#     cursor.execute(query)
#     result = cursor.fetchall()

#     if result:
#         return {"startups" : startups}

#     else:
#         raise HTTPException(status_code=404, detail="No startup listed.")


#     # nje funksionalitet qe ti marri nga me i vjetri te me i riu


# #updating a startup
# @router.put("/update/{id}")
# async def update(id : int , startup_new : StartUp):
#     for index, startup in enumerate(startups):
#         if startup.id == id:
#             startups[index] = startup_new
#             return {"startup": startup_new}

#     return {"No startup found to update"}


# # @router.put("/update/{id}")
# # async def update_startup(id: int , updated_startup : dict):
# #     for startup in startups:
# #         if startup['id'] == id:


# @router.delete("/{name}")
# async def delete_startup_name(name : str):
#     for startup in startups:
#         if startup.name == name:
#             startups.remove(startup)
#             return {"StartUp sucessfully deleted by its name."}


#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Startup not found"
#     )


# #deleting a single startup
# @router.delete("/{id}")
# async def delete(id : int):
#     for startup in startups:
#         if startup.id == id:
#             startups.remove(startup)

#             return {"message" : "Startup has been deleted"}


#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Startup not found"
#     )


# return {"message" : "Startup not found"} - this doesnt do anything , use raise
