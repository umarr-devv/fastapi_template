from fastapi import WebSocket, WebSocketDisconnect, APIRouter

router = APIRouter(prefix='/default')


@router.websocket('/')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ...
