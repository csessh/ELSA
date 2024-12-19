# ELSA
ELSA SPEAK's coding challenge

## Introduction

## Pre-requisite:

The following tools are required:

- Docker
- Redis

### Redis 

This is a standard Redis installation. It can be done with either Docker or your favourite package manager (Brew, DNF, Snap...):

``` bash
$ docker run -p 6379:6379 redis/redis-stack:latest
```

or 

```bash
$ sudo dnf install redis
$ sudo systemctl start redis
```

Once installed, validate with `redis-cli`:

``` bash
$ redis-cli ping
PONG
```

## Server 

To get the server started, run the following command:

``` bash
$ docker compose up
```

`compose.yaml` defines two containers: `ElsaServer` and `Redis`

`ElsaServer` is a FastAPI server exposed to port `8000` on `localhost`.
`Redis` is mapped to `6379`.

## Client simulation
