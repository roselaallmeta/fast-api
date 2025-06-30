import asyncpg

pool = None



async def get_connection():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            user='admin',
            password='rosi123',
            database='main',
            host='localhost',
            port=5433
        )
        
    return pool
