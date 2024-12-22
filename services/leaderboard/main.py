from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List

from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
from loguru import logger
from nats.aio.client import Client as NATS
from redis import ConnectionPool, StrictRedis
from starlette.responses import FileResponse

from utils.connections import ConnectionManager

ws_connection_manager = ConnectionManager()
redis_client = StrictRedis(connection_pool=ConnectionPool().from_url("redis://localhost:6379"))
nc = NATS()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    global nc

    try:

        async def subscribe_handler(msg):
            subject = msg.subject
            reply = msg.reply
            data = msg.data.decode()
            logger.info(f"Received a message on '{subject} {reply}': {data}")

        await nc.connect("localhost")
        await nc.subscribe(subject="LEADERBOARD.*", cb=subscribe_handler)

        yield
    finally:
        if redis_client:
            redis_client.close()

        if nc:
            await nc.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get():
    return FileResponse("templates/home.html")


@app.websocket_route("/scoreboard")
async def scores(websocket: WebSocket):
    await ws_connection_manager.connect(websocket)
    try:
        while True:
            data = query_scoreboard_from_cache()
            await ws_connection_manager.broadcast_json(data)
    except WebSocketDisconnect:
        ws_connection_manager.disconnect(websocket)


def query_scoreboard_from_cache() -> List[Dict[str, Any]]:
    z_scores = redis_client.zrevrange(name="quiz_uuid", start=0, end=-1, withscores=True)
    return [{"PlayerID": s[0].decode(), "Score": s[1], "Rank": i + 1} for i, s in enumerate(z_scores)]
