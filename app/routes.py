from fastapi import APIRouter, HTTPException, BackgroundTasks
from .models import Contact, ContactCreate, ContactPatch
import asyncio, pathlib, time
from typing import Dict, List

router = APIRouter()

# in-memory store
contacts: Dict[int, Contact] = {}
_next_id = 1
lock = asyncio.Lock()

#@router.get("/", tags=["system"])
#def root():
#    return {"status": "ok", "app": "Contacts API Demo (Vite Frontend)"}
@router.get("/api/health", tags=["system"])
def health():
    return {"status": "ok", "app": "Contacts API Demo (Vite Frontend)"}

@router.get("/slow", tags=["demo"])
async def slow(seconds: int = 2):
    await asyncio.sleep(seconds)
    return {"msg": f"waited {seconds} seconds"}

def heavy_job(name: str):
    time.sleep(3)
    log_path = pathlib.Path(__file__).parent.parent / "job.log"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"[done] hello {name}\n")

@router.post("/bg", tags=["demo"])
def run_bg(name: str, tasks: BackgroundTasks):
    tasks.add_task(heavy_job, name)
    return {"queued": True, "name": name}

# CRUD
@router.get("/api/contacts", response_model=List[Contact])
async def list_contacts():
    return list(contacts.values())

@router.get("/api/contacts/{cid}", response_model=Contact)
async def get_contact(cid: int):
    c = contacts.get(cid)
    if not c: raise HTTPException(404, "not found")
    return c

@router.post("/api/contacts", response_model=Contact, status_code=201)
async def create_contact(data: ContactCreate):
    global _next_id
    async with lock:
        cid = _next_id
        _next_id += 1
        c = Contact(id=cid, **data.model_dump())
        contacts[cid] = c
        return c

@router.put("/api/contacts/{cid}", response_model=Contact)
async def replace_contact(cid: int, data: ContactCreate):
    async with lock:
        if cid not in contacts: raise HTTPException(404, "not found")
        c = Contact(id=cid, **data.model_dump())
        contacts[cid] = c
        return c

@router.patch("/api/contacts/{cid}", response_model=Contact)
async def patch_contact(cid: int, data: ContactPatch):
    async with lock:
        if cid not in contacts: raise HTTPException(404, "not found")
        updated = contacts[cid].model_copy(update=data.model_dump(exclude_unset=True))
        contacts[cid] = updated
        return updated

@router.delete("/api/contacts/{cid}", status_code=204)
async def delete_contact(cid: int):
    async with lock:
        if cid in contacts:
            del contacts[cid]; return
        raise HTTPException(404, "not found")
