from contextlib import asynccontextmanager
from typing import AsyncGenerator

import nats
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketDisconnect
from nats.js import JetStreamContext
from redis.asyncio import Redis as AsyncRedis
from websockets.exceptions import ConnectionClosed

from common.connections import WSConnectionManager

ws_manager = WSConnectionManager()
redis = AsyncRedis.from_url("redis://localhost:6379")
jetstream = None


async def get_jetstream_context() -> JetStreamContext:
    global jetstream

    if not jetstream:
        nc = await nats.connect("nats://localhost:4222")
        jetstream = nc.jetstream()

    return jetstream


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    js = await get_jetstream_context()
    await js.add_stream(name="livescore", subjects=["LEADERBOARD.*"])

    yield
    await redis.aclose()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates("templates")


@app.get("/livescore/{quiz_id}", response_class=HTMLResponse)
async def livescore(request: Request, quiz_id: str):
    return templates.TemplateResponse(request=request, name="leaderboard.html", context={"qid": quiz_id})


@app.websocket("/livescore/{quiz_id}")
async def livescore_websocket(ws: WebSocket, quiz_id: str):
    await ws_manager.connect(session=quiz_id, websocket=ws)
    js = await get_jetstream_context()
    consumer = await js.subscribe(subject=f"LEADERBOARD.{quiz_id}")

    while True:
        try:
            msg = await consumer.next_msg(timeout=None)
            await msg.ack()

            zscores = await redis.zrevrange(name=quiz_id, start=0, end=-1, withscores=True)
            data = [{"PlayerID": s[0].decode(), "Score": s[1], "Rank": i + 1} for i, s in enumerate(zscores)]

            await ws_manager.broadcast_json(session=quiz_id, data=data)
        except (WebSocketDisconnect, ConnectionClosed, RuntimeError):
            ws_manager.disconnect(session=quiz_id, websocket=ws)
            break
