from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Body
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []
    
    
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)
        print("Client connected, total:", len(self.active))
    

    async def disconnect(self, ws: WebSocket):
        self.active.remove(ws)
        print("Client disconnected, total:", len(self.active))


    async def broadcast(self, msg: dict):
        for ws in self.active:
            await ws.send_json(msg)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(ws)
    finally:
        await manager.disconnect(ws)


@app.post("/publish")
async def publish_event(payload: dict = Body(...)):
    await manager.broadcast(payload)
    return {"status": "ok"}