import asyncpg
import time
from ..config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT
from ..log import log

pool = None
time_out_min = 1
time_out_max = 30
time_out_step = 5

async def init_pool():
    condition = True
    while(condition):
        try:
            global pool
            pool = await asyncpg.create_pool(
                host=DB_HOST,
                port=DB_PORT,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                min_size=1,  
                max_size=10  
            )
            print("Connection to the database is established\n")
            condition = False
        except Exception as e:
            print(f"Failed to connect to the database:\n{e}")


@log.async_logger
async def close_pool():
    if pool:
        await pool.close()