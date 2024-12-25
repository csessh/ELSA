# ELSA

ELSA SPEAK's coding challenge

1. [Introduction](README#Introduction)


## Introduction

In this repo, you'll find:

- a high level design breakdown for a real-time quiz feature for an English learning application.
- a working demo for the live update leaderboard written in Python. 
- an instruction to run the demo.

TODO: Table of Contents


## Technical demo

In this demo, I've chosen to focus on the `real-time leaderboard` component of the system.

The score updates and user participation are mocked with a simulation.

### Setup

To run this demo, execute the following commands:

``` bash
docker compose build
docker compose up -d # omit -d to trace logs
```

This demo's `compose.yaml` builds and creates the following four components:

- Leaderboard service, a FastAPI server
- Quiz service simulation
- Nats Jetstream, a lightweight message broker
- Redis

To quickly verify that all services are up, use `docker ps`:

``` bash
fw13 :: ~/ELSA ‹main*› » docker ps
CONTAINER ID   IMAGE                      COMMAND                  CREATED         STATUS         PORTS     NAMES
95073b94d88c   elsa-quiz_sim              "uv run services/qui…"   3 seconds ago   Up 3 seconds             simulation
a8e16bf85c83   elsa-leaderboard           "uv run fastapi run …"   3 seconds ago   Up 3 seconds             leaderboard
4ff689ee565e   redis/redis-stack:latest   "/entrypoint.sh"         3 seconds ago   Up 3 seconds             redis
b25077cdb47f   nats:2.10.24               "/nats-server -js -m…"   3 seconds ago   Up 3 seconds             broker
```

To clean up:

``` bash
docker compose down
```

It's worth noting that:

- Nothing is persisted to disc.
- These containers operate in `host` network mode.
- They take up the following ports:
    - 8000 (Leaderboard service)
    - 4222 (Nats server)
    - 8222 (Nats monitoring)
    - 6379 (Redis)

### Quiz simulation

### Leaderboard

The leaderboard is accessible via `localhost:8000/lovescore/{quiz_name}`.

This can either be via a browser: 

![image](./docs/leaderboard.png)

or via `wscat` in your terminal:

``` bash
$ wscat -c ws://localhost:8000/livescore/quiz_1 

Connected (press CTRL+C to quit)
< [
    {"PlayerID":"player1","Score":158.0,"Rank":1},
    {"PlayerID":"player6","Score":155.0,"Rank":2},
    {"PlayerID":"player8","Score":146.0,"Rank":3},
    {"PlayerID":"player0","Score":146.0,"Rank":4},
    {"PlayerID":"player2","Score":145.0,"Rank":5},
    {"PlayerID":"player5","Score":140.0,"Rank":6},
    {"PlayerID":"player7","Score":139.0,"Rank":7},
    {"PlayerID":"player9","Score":137.0,"Rank":8},
    {"PlayerID":"player3","Score":136.0,"Rank":9},
    {"PlayerID":"player4","Score":118.0,"Rank":10}
]
...
```

### Redis

### Message broker (Nats)


## System design

![image](./docs/high_level_design_diagram.png)

### Assumptions

### Challenges

### Components

### Workflows

### Further consideration

## Happy holidays
