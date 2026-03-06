import uvicorn
import asyncio
from include.api import app
from include.db import db_connect as db

async def run_server():
    try:
        await db.init_pool()
        
        config = uvicorn.Config("main:app", host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        await server.serve()
        
    finally:
        if db.pool:
            await db.close_pool()

if __name__ == '__main__':
    asyncio.run(run_server())