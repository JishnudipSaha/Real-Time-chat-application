from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import models, database, manager
from fastapi import HTTPException
import os

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Use absolute path detection for the static folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")

# Mount using the absolute path
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def get():
    # Points directly to index.html inside chat_app/static/
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        with open(index_file) as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="index.html not found in static folder", status_code=404)

@app.websocket("/ws/{room_id}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str, db: Session = Depends(get_db)):
    await manager.manager.connect(websocket, room_id)
    
    # History fetch
    history = db.query(models.Message).filter(models.Message.room_id == room_id).order_by(models.Message.timestamp.asc()).all()
    for msg in history:
        await websocket.send_json({"user": "History", "msg": msg.content})

    try:
        while True:
            data = await websocket.receive_text()
            # Added a default or searched user_id so the DB doesn't crash
            new_msg = models.Message(content=data, room_id=room_id)
            db.add(new_msg)
            db.commit()
            
            await manager.manager.broadcast({"user": username, "msg": data}, room_id)
    except WebSocketDisconnect:
        manager.manager.disconnect(websocket, room_id)
