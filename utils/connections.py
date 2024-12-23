from collections import defaultdict
from typing import Any, Dict, List

from fastapi import WebSocket, websockets
from loguru import logger


class WSConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, session: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[session].append(websocket)

    def disconnect(self, session: str, websocket: WebSocket):
        self.active_connections[session].remove(websocket)

    async def broadcast(self, session: str, message: str):
        for connection in self.active_connections.get(session, []):
            await connection.send_text(message)

    async def broadcast_json(self, session: str, data: Any):
        for connection in self.active_connections.get(session, []):
            await connection.send_json(data)
