import logging
from typing import Dict, List
from fastapi import WebSocket

import logging

logger = logging.getLogger(__name__)


class BaseSocketManager:
    def __init__(self):
        # Store connections by room_id
        self.rooms: Dict[int, List[Dict[str, WebSocket]]] = {}

    async def connect(self, websocket: WebSocket, uuid: str, room_id: int):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        self.rooms[room_id].append({"uuid": uuid, "websocket": websocket})
        logger.info(f"User {uuid} connected to room {room_id}.")

    async def disconnect(self, websocket: WebSocket):
        for room_id, connections in self.rooms.items():
            self.rooms[room_id] = [
                conn for conn in connections if conn["websocket"] != websocket
            ]
            if not self.rooms[room_id]:
                del self.rooms[room_id]
                logger.info(f"Room {room_id} is now empty.")
                break

    async def send_personal_message(self, data, websocket: WebSocket):
        try:
            await websocket.send_json(data)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def broadcast(self, data, room_id: int):
        if room_id not in self.rooms:
            logger.error(f"Room {room_id} does not exist.")
            return
        for connection in self.rooms[room_id]:
            try:
                await connection["websocket"].send_json(data)
            except Exception as e:
                logger.error(f"Error broadcasting message to room {room_id}: {e}")
                await self.disconnect(connection["websocket"])


socket_manager = BaseSocketManager()
