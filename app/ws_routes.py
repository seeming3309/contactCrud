from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketState

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_text("connected. type something!")
    try:
        while True:
            msg = await ws.receive_text()
            await ws.send_text(f"echo: {msg}")
    except WebSocketDisconnect:
        pass
    finally:
        if (getattr(ws, "application_state", None) != WebSocketState.DISCONNECTED and
            getattr(ws, "client_state", None) != WebSocketState.DISCONNECTED):
            try: await ws.close()
            except: pass
