from contextlib import asynccontextmanager
from typing import AsyncGenerator

import nats
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketDisconnect
from loguru import logger
from nats.js import JetStreamContext
from redis.asyncio import Redis
from websockets.exceptions import ConnectionClosed

from utils.connections import WSConnectionManager

ws_connection_manager = WSConnectionManager()
redis = Redis.from_url("redis://localhost:6379", auto_close_connection_pool=False)
jetstream = None


async def get_jetstream_context() -> JetStreamContext:
    global jetstream

    if not jetstream:
        nc = await nats.connect()
        jetstream = nc.jetstream()

    return jetstream


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    js = await get_jetstream_context()
    await js.add_stream(name="elsa", subjects=["LEADERBOARD.*"])

    yield

    logger.info("FastAPI shutting down ... ")
    await redis.aclose()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates("templates")


@app.get("/livescore/{quiz_id}", response_class=HTMLResponse)
async def home(request: Request, quiz_id: str):
    # TODO: Validate quiz_id against active sessions in Redis, defaults to sqlite
    # Return 404 if nothing matches
    # Return template home.html with session id
    return templates.TemplateResponse(request=request, name="home.html", context={"qid": quiz_id})


@app.websocket("/livescore/{quiz_id}")
async def scores(ws: WebSocket, quiz_id: str):
    await ws_connection_manager.connect(session=quiz_id, websocket=ws)
    js = await get_jetstream_context()
    consumer = await js.subscribe(subject=f"LEADERBOARD.{quiz_id}")

    while True:
        try:
            # TODO: Check msg content (timestamp) and compare to current timestamp
            await consumer.next_msg(None)

            z_scores = await redis.zrevrange(name=quiz_id, start=0, end=-1, withscores=True)
            data = [{"PlayerID": s[0].decode(), "Score": s[1], "Rank": i + 1} for i, s in enumerate(z_scores)]
            await ws_connection_manager.broadcast_json(session=quiz_id, data=data)
        except (WebSocketDisconnect, ConnectionClosed, RuntimeError):
            ws_connection_manager.disconnect(session=quiz_id, websocket=ws)
            break
