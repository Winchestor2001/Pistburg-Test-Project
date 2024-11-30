import logging

from fastapi import WebSocket
from fastapi.routing import APIRouter
from starlette.websockets import WebSocketDisconnect

from src.apps.api.auth.jwt_conf import JwtBearer
from src.apps.websocket.socket_manager import socket_manager

ws = APIRouter(prefix="/ws")
jwt_bearer = JwtBearer()
logger = logging.getLogger(__name__)


@ws.websocket("/support/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    token = websocket.query_params.get("token")
    logger.info(f"Token received: {token}")
    if not token:
        logger.error("Token missing.")
        await websocket.close(code=4000, reason="Token missing")
        return

    try:
        token_payload = jwt_bearer.verify_access_token(token)
        if not token_payload:
            logger.error("Invalid token.")
            await websocket.close(code=4001, reason="Invalid token")
            return
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        await websocket.close(code=4002, reason="Token validation failed")
        return

    user_uuid = token_payload.get("uuid")
    logger.info(f"User {user_uuid} connected to room {room_id}.")
    await socket_manager.connect(websocket, user_uuid, room_id)

    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received data from {user_uuid} in room {room_id}: {data}")
            await socket_manager.broadcast(data, room_id)
    except WebSocketDisconnect:
        logger.info(f"User {user_uuid} disconnected from room {room_id}.")
    except Exception as e:
        logger.error(f"Connection error for user {user_uuid}: {e}")
    finally:
        await socket_manager.disconnect(websocket)
