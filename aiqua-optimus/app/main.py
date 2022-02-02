from datetime import datetime, time
from typing import Optional

from fastapi import FastAPI, HTTPException


DOORS = [
    {
        "id": 1,
        "name": "Front Door",
        "ip_address": "192.168.1.1",
    },
    {
        "id": 2,
        "name": "Back Door",
        "ip_address": "192.168.1.2",
    },
]

TAGS = [
    {
        "id": 1,
        "number": "FFFFF7",
        "enabled": True,
    },
    {
        "id": 2,
        "number": "FDF7DF",
        "enabled": False,
    },
    {
        "id": 3,
        "number": "FFB7EF",
        "enabled": True,
    },
    {
        "id": 4,
        "number": "EFB77E",
        "enabled": True,
    },
]

SCHEDULES = [
    {
        "id": 1,
        "door_id": 1,
        "tag_id": 1,
        "start": time(hour=0, minute=0, second=0),
        "end": time(hour=23, minute=59, second=59),
    },   
    {
        "id": 2,
        "door_id": 1,
        "tag_id": 3,
        "start": time(hour=9, minute=0, second=0),
        "end": time(hour=17, minute=0, second=0),
    },   
    {
        "id": 3,
        "door_id": 2,
        "tag_id": 4,
        "start": time(hour=18, minute=0, second=0),
        "end": time(hour=23, minute=0, second=0),
    },   
]

ACCESS_LOGS = [
]


app = FastAPI()

@app.get("/doors")
def read_doors():
    return DOORS

@app.get("/doors/{door_id}")
def read_door(door_id: int):
    try:
        return [d for d in DOORS if d['id'] == door_id][0]
    except IndexError:
        raise HTTPException(status_code = 404, detail=  "Id not found")

@app.get("/tags")
def read_tags():
    return TAGS

@app.get("/tags/{tag_id}")
def read_tag(tag_id: int):
    try:
        return [t for t in TAGS if t['id'] == tag_id][0]
    except IndexError:
        raise HTTPException(status_code = 404, detail=  "Id not found")

@app.get("/schedules")
def read_schedules(door_id: Optional[int]=None, tag_id: Optional[str]=None):
    if door_id == None and tag_id == None: return SCHEDULES
    if door_id == None: return [s for s in SCHEDULES if s['tag_id'] == tag_id]
    if tag_id == None: return [s for s in SCHEDULES if s['door_id'] == door_id]

@app.get("/schedules/{schedule_id}")
def read_schedule(schedule_id: int):
    return [t for t in SCHEDULES if t['id'] == schedule_id][0]

@app.get("/access_logs")
def read_access_logs():
    return ACCESS_LOGS

@app.post("/access_logs")
def write_access_log(tag_id: str, granted: bool, door_id: Optional[int]=None, timestamp: Optional[datetime]=datetime.now()):
    """
    - **door_id:** if not provided, `door_id` is determined by the requesting IP address.
    - **timestamp:** if not provided, the date and time when the request is made is used.
    """
    # This would normally lookup door based on the source IP of the request.
    if door_id == None: door_id = 1
    ACCESS_LOGS.append({
        "tag_id": tag_id,
        "door_id": door_id,
        "granted": granted,
        "timestamp": timestamp,
    })
