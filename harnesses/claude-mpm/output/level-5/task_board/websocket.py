"""WebSocket connection manager."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import DefaultDict
from collections import defaultdict
import json

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.connections: DefaultDict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, board_id: int, ws: WebSocket):
        await ws.accept()
        self.connections[board_id].append(ws)

    def disconnect(self, board_id: int, ws: WebSocket):
        if ws in self.connections[board_id]:
            self.connections[board_id].remove(ws)

    async def broadcast(self, board_id: int, event: str, data: dict):
        msg = json.dumps({"event": event, "data": data})
        dead = []
        for ws in list(self.connections[board_id]):
            try:
                await ws.send_text(msg)
            except Exception:
                dead.append(ws)
        for ws in dead:
            if ws in self.connections[board_id]:
                self.connections[board_id].remove(ws)


manager = ConnectionManager()


@router.websocket("/ws/{board_id}")
async def websocket_endpoint(board_id: int, websocket: WebSocket):
    await manager.connect(board_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(board_id, websocket)
