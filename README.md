# ELSA

ELSA SPEAK's coding challenge

## Introduction

## Technical demo

### Setup

Every components, simulation included, are packaged with `Docker`.

``` bash
docker compose build
docker compose up -d # omit -d to trace logs
```

### Leaderboard

The leaderboard is represented with JSON

For example:

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

