#!/usr/bin/env bash
set -euo pipefail

echo ">>> تحديث الحزم (Termux)"
pkg update -y || true
pkg upgrade -y || true

echo ">>> تثبيت المتطلبات..."
pkg install -y python git nano || true

echo ">>> ترقية pip..."
pip install --upgrade pip wheel setuptools

echo ">>> تثبيت مكتبات Python المطلوبة..."
pip install --no-cache-dir fastapi uvicorn httpx

echo ">>> إنشاء خادم Eleanor 🤺 Auto Assistant"
cat > eleanor_auto.py <<'PY'
#!/usr/bin/env python3
# Eleanor 🤺 Auto Assistant - نسخة Termux موحدة
# الغرف تتصل تلقائيًا بالمساعد الداخلي كل 30 ثانية لتبادل التحليلات والنبضات

import os, asyncio, json, datetime, csv
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

APP_NAME = "Eleanor 🤺 Auto Assistant"
LEDGER_FILE = "ledger.csv"
POLL_INTERVAL = 30.0  # ثانية بين كل نبضة تلقائية
ROOMS: Dict[str, Dict[str, Any]] = {}
ROOM_TASKS: Dict[str, asyncio.Task] = {}

app = FastAPI(title=APP_NAME)

# 🔹 التهيئة التلقائية
def ensure_ledger():
    if not os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "w", newline="", encoding="utf-8") as f:
            f.write("timestamp,type,room,detail\n")

def ledger_log(evt_type: str, room: str, detail: Any):
    ensure_ledger()
    ts = datetime.datetime.utcnow().isoformat()
    with open(LEDGER_FILE, "a", encoding="utf-8") as f:
        f.write(f'{ts},{evt_type},{room},"{json.dumps(detail, ensure_ascii=False)}"\n')

class CreateRoomIn(BaseModel):
    room_id: str
    meta: Dict[str, Any] = {}

# 🔹 المساعد الداخلي (محاكاة تحليل ذكي)
def internal_assistant(room_id: str, text: str) -> Dict[str, Any]:
    t = text.lower()
    if "تحليل" in t or "sim" in t:
        return {"reply": f"تحليل الغرفة {room_id}: السيولة مستقرة، لا مشاكل حالياً.", "action": "none"}
    if "اختراق" in t or "هجوم" in t:
        return {"reply": f"🚨 تم رصد نشاط مريب في {room_id}. تم تنبيه bibAhhhh1.", "action": "alert_security"}
    return {"reply": f"نبضة من {room_id}: كل الأنظمة تعمل بكفاءة.", "action": "none"}

# 🔹 العامل التلقائي لكل غرفة
async def room_worker(room_id: str, interval: float):
    ledger_log("worker_started", room_id, {"interval": interval})
    try:
        while True:
            message = f"نبضة {room_id} - طلب تحليل دوري"
            resp = internal_assistant(room_id, message)
            ledger_log("assistant_response", room_id, resp)
            if resp.get("action") == "alert_security":
                ledger_log("security_alert", room_id, {"note": "سيتم إخطار bibAhhhh1"})
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        ledger_log("worker_stopped", room_id, {"reason": "cancelled"})
        return

# 🔹 نقاط التشغيل API
@app.on_event("startup")
async def startup_event():
    ensure_ledger()
    ledger_log("app_startup", "system", {"interval": POLL_INTERVAL})

@app.post("/rooms/create")
async def create_room(data: CreateRoomIn):
    if data.room_id in ROOMS:
        raise HTTPException(status_code=400, detail="room_exists")
    ROOMS[data.room_id] = {"meta": data.meta, "created": datetime.datetime.utcnow().isoformat(), "connected": False}
    ledger_log("room_created", data.room_id, data.meta)
    return {"status": "ok", "room": data.room_id}

@app.post("/rooms/{room_id}/connect")
async def connect_room(room_id: str):
    if room_id not in ROOMS:
        raise HTTPException(status_code=404, detail="room_not_found")
    if room_id in ROOM_TASKS and not ROOM_TASKS[room_id].done():
        return {"status": "already_connected"}
    task = asyncio.create_task(room_worker(room_id, POLL_INTERVAL))
    ROOM_TASKS[room_id] = task
    ROOMS[room_id]["connected"] = True
    ledger_log("room_connected", room_id, {})
    return {"status": "connected", "room": room_id}

@app.post("/rooms/{room_id}/disconnect")
async def disconnect_room(room_id: str):
    if room_id not in ROOMS:
        raise HTTPException(status_code=404, detail="room_not_found")
    task = ROOM_TASKS.get(room_id)
    if task:
        task.cancel()
        ROOM_TASKS.pop(room_id, None)
    ROOMS[room_id]["connected"] = False
    ledger_log("room_disconnected", room_id, {})
    return {"status": "disconnected", "room": room_id}

@app.get("/rooms")
async def list_rooms():
    return {"rooms": list(ROOMS.keys()), "connected": [r for r, t in ROOM_TASKS.items() if not t.done()]}

@app.get("/ledger")
async def get_ledger(limit: int = 200):
    ensure_ledger()
    with open(LEDGER_FILE, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()[-limit:]
    return {"entries": lines}

@app.get("/health")
async def health():
    return {"status": "ok", "rooms": len(ROOMS), "connected": len(ROOM_TASKS)}

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 {APP_NAME} قيد التشغيل على http://127.0.0.1:9001")
    uvicorn.run("eleanor_auto:app", host="127.0.0.1", port=9001, log_level="info")
PY

chmod +x eleanor_auto.py
echo ">>> بدء التشغيل..."
python eleanor_auto.py
