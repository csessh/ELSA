from typing import Dict, List
from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
from redis import ConnectionPool, StrictRedis
from starlette.responses import FileResponse
from services.common.connections import ConnectionManager


app = FastAPI()
r = StrictRedis(connection_pool=ConnectionPool().from_url("redis://localhost:6379"))
manager = ConnectionManager()

INIT = False


@app.get("/")
async def get():
    global INIT

    if not INIT:
        set_scoreboard()
    return FileResponse("templates/home.html")


@app.websocket_route("/scores")
async def scores(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = get_scores()
            await websocket.send_json(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


def set_scoreboard():
    for i in range(1, 20):
        r.zadd(name="quiz_uuid", mapping={f"player{i}": 0})


def get_scores() -> List[Dict[str, int]]:
    z_scores = r.zrevrange(name="quiz_uuid", start=0, end=-1, withscores=True)
    return [{"PlayerID": s[0].decode(), "Score": s[1], "Rank": i + 1} for i, s in enumerate(z_scores)]
