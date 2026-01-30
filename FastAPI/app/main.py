from fastapi import FastAPI, HTTPException
from .models import TicketCreate, TicketStore

app = FastAPI(title="Support API")
store = TicketStore()

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tickets")
def list_tickets():
    return store.list_tickets()


@app.post("/tickets", status_code=201)
def create_ticket(payload: TicketCreate):
    if payload.priority not in {"low", "medium", "high"}:
        raise HTTPException(status_code=400, detail="priority must be low|medium|high")

    duplicate = store.find_recent_duplicate(payload.subject, window_minutes=5)
    if duplicate:
        raise HTTPException(
            status_code=409,
            detail=f"ticket already created recently (id={duplicate.id})",
        )

    return store.create_ticket(payload.subject, payload.priority)
#Demo
