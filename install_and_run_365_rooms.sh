#!/usr/bin/env bash
set -euo pipefail

echo ">>> إعداد البيئة... (Termux)"
# تحديث الحزم (لن يفشل إن لم يتوفر repo)
pkg update -y || true
pkg upgrade -y || true

echo ">>> تثبيت python وأدوات أساسية..."
pkg install -y python git nano || true

echo ">>> ترقية pip..."
python -m pip install --upgrade pip setuptools wheel

echo ">>> تثبيت مكتبات Python المطلوبة..."
python -m pip install --no-cache-dir fastapi uvicorn[standard] websockets aiofiles rich

echo ">>> إنشاء مشروع Eleanor Rooms (365 غرفة)..."
rm -rf ~/EleanorRooms
mkdir -p ~/EleanorRooms
cd ~/EleanorRooms

cat > app.py <<'PY'
#!/usr/bin/env python3
import asyncio, random, json, os, datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

APP = FastAPI(title="Eleanor Mini 365 Rooms", docs_url="/docs")

DATA_DIR = os.path.join(os.path.dirname(__file__),"data")
os.makedirs(DATA_DIR, exist_ok=True)
LEDGER = os.path.join(DATA_DIR,"room_ledger.csv")

# create ledger header if not exists
if not os.path.exists(LEDGER):
    with open(LEDGER,"w",encoding="utf-8") as f:
        f.write("timestamp,room_id,event,detail\n")

ROOM_COUNT = 365

class RoomStatus(BaseModel):
    room_id: int
    status: str
    last_heartbeat: str
    subscribers: int

# Simple in-memory manager
class RoomManager:
    def __init__(self, n):
        self.n = n
        # store last heartbeat ISO timestamp
        self.rooms = {i: {"last_heartbeat": None, "status":"idle", "subs":0} for i in range(1,n+1)}
        # mapping room_id -> set(WebSocket)
        self.subscribers = {i:set() for i in range(1,n+1)}
        self.lock = asyncio.Lock()
    async def set_heartbeat(self, room_id, note="tick"):
        ts = datetime.datetime.utcnow().isoformat()
        async with self.lock:
            self.rooms[room_id]["last_heartbeat"] = ts
            self.rooms[room_id]["status"] = "active"
        # write ledger
        with open(LEDGER,"a",encoding="utf-8") as f:
            f.write(f"{ts},{room_id},heartbeat,{note}\\n")
        # notify subscribers
        await self.notify_subscribers(room_id, {"type":"heartbeat","room":room_id,"ts":ts,"note":note})
    async def notify_subscribers(self, room_id, msg: dict):
        websockets = list(self.subscribers.get(room_id, set()))
        remove = []
        for ws in websockets:
            try:
                await ws.send_json(msg)
            except Exception:
                remove.append(ws)
        # cleanup dead sockets
        if remove:
            async with self.lock:
                for ws in remove:
                    if ws in self.subscribers.get(room_id,set()):
                        self.subscribers[room_id].remove(ws)
    async def subscribe(self, room_id, ws: WebSocket):
        await ws.accept()
        async with self.lock:
            self.subscribers[room_id].add(ws)
            self.rooms[room_id]["subs"] = len(self.subscribers[room_id])
    async def unsubscribe(self, room_id, ws: WebSocket):
        async with self.lock:
            if ws in self.subscribers.get(room_id,set()):
                self.subscribers[room_id].remove(ws)
            self.rooms[room_id]["subs"] = len(self.subscribers[room_id])
    def get_status(self, room_id):
        r = self.rooms.get(room_id)
        if not r:
            raise KeyError("room not found")
        return {"room_id":room_id,"status":r["status"],"last_heartbeat":r["last_heartbeat"],"subscribers":r["subs"]}

manager = RoomManager(ROOM_COUNT)

# Background task: spawn a coroutine per room to simulate heartbeats
async def room_worker(room_id):
    while True:
        # random sleep to simulate activity (between 10 and 90 seconds)
        await asyncio.sleep(10 + random.random() * 80)
        await manager.set_heartbeat(room_id, note="auto_tick")

@APP.on_event("startup")
async def startup_event():
    # launch all room workers
    for i in range(1, ROOM_COUNT+1):
        asyncio.create_task(room_worker(i))

# REST endpoints
@APP.get("/rooms/{room_id}/status", response_model=RoomStatus)
async def room_status(room_id: int):
    if room_id < 1 or room_id > ROOM_COUNT:
        raise HTTPException(status_code=404, detail="room not found")
    s = manager.get_status(room_id)
    return s

@APP.post("/rooms/{room_id}/heartbeat")
async def room_heartbeat(room_id:int):
    if room_id < 1 or room_id > ROOM_COUNT:
        raise HTTPException(status_code=404, detail="room not found")
    await manager.set_heartbeat(room_id, note="manual_trigger")
    return JSONResponse({"status":"ok","room":room_id})

@APP.get("/rooms")
async def list_rooms():
    out=[]
    for i in range(1, ROOM_COUNT+1):
        out.append(manager.get_status(i))
    return out

@APP.get("/ledger")
async def ledger(limit:int=200):
    if not os.path.exists(LEDGER):
        return {"entries":[]}
    with open(LEDGER,encoding="utf-8") as f:
        lines = f.read().splitlines()
    return {"entries": lines[-limit:]}

# WebSocket subscription per room
@APP.websocket("/ws/rooms/{room_id}")
async def websocket_room(ws: WebSocket, room_id:int):
    if room_id < 1 or room_id > ROOM_COUNT:
        await ws.close(code=1008)
        return
    await manager.subscribe(room_id, ws)
    try:
        while True:
            # keep connection open, we don't expect messages from client but accept pings
            data = await ws.receive_text()
            # echo back simple ack
            await ws.send_json({"type":"ack","received":data})
    except WebSocketDisconnect:
        await manager.unsubscribe(room_id, ws)
    except Exception:
        await manager.unsubscribe(room_id, ws)

# lightweight root
@APP.get("/")
async def root():
    return {"app":"Eleanor Mini 365 Rooms", "rooms": ROOM_COUNT, "docs":"/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:APP", host="0.0.0.0", port=8000, log_level="info")
PY

echo ">>> إعطاء الأذونات وتشغيل الخادم..."
chmod +x app.py

# حاول تشغيل uvicorn في الخلفية إن أمكن
if command -v nohup >/dev/null 2>&1; then
  nohup python app.py > /dev/null 2>&1 &
  sleep 1
  echo ">>> الخادم بدأ في الخلفية. افتح http://127.0.0.1:8000/docs"
else
  echo ">>> لا يوجد nohup، سيتم تشغيل الخادم بصورة تفاعلية الآن."
  python app.py
fi

