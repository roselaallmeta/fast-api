from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routers import (
    # industries,
    # investment_validation,
    # ventures,
    user,
    # user_profiles,
    investments,
)

from .src.commons.postgres import database
import uvicorn
from fastapi import FastAPI


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#      await database.connect()
#    yield
#     await database.disconnect()
#     pool = await asyncpg.create_pool(dsn=DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(investments.router)

# app.include_router(industries.router)
# app.include_router(investment_validation.router)
# app.include_router(ventures.router)
# app.include_router(user_profiles.router)
# app.include_router(investments.router)

# app.include_router(user_profiles.router)

if __name__ == "__main__ ":
    uvicorn.run(app, host="8000")

# ctlr + c ngeci
