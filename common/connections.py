from collections import defaultdict
from redis.asyncio import Redis
from typing import Any, Dict, List

from fastapi import WebSocket


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class WSConnectionManager(metaclass=Singleton):
    """
    A simple websocket connection manager to keep track of active conntions.
    """

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, session: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[session].append(websocket)

    def disconnect(self, session: str, websocket: WebSocket):
        self.active_connections[session].remove(websocket)

    async def broadcast_json(self, session: str, data: Any):
        for connection in self.active_connections.get(session, []):
            await connection.send_json(data)
