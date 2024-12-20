import time
import random
from fastapi import FastAPI
from redis import ConnectionPool, StrictRedis
from starlette.responses import FileResponse, JSONResponse


app = FastAPI()
r = StrictRedis(connection_pool=ConnectionPool().from_url("redis://localhost:6379"))


@app.get("/")
async def get():
    set_scoreboard()
    return FileResponse("templates/home.html")


@app.route("/scores")
async def scores(data):
    return JSONResponse(content=get_scores())


def set_scoreboard():
    for i in range(1, 10):
        r.zadd(name="quiz_uuid", mapping={f"player{i}": 0})


def get_scores():
    z_scores = r.zrange(name="quiz_uuid", start=0, end=-1, withscores=True)
    return [{"id": score[0].decode(), "score": score[1]} for score in z_scores]


def simulation():
    while True:
        for i in range(1, 10):
            r.zincrby("quiz_uuid", value=f"player{i}", amount=random.randint(-10, 20))
        time.sleep(2)


if __name__ == "__main__":
    simulation()
