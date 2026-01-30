from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel


class TicketCreate(BaseModel):
    subject: str
    priority: str


class Ticket(BaseModel):
    id: int
    subject: str
    priority: str
    created_at: datetime


class TicketStore:
    def __init__(self):
        self._tickets: List[Ticket] = []
        self._next_id = 1

    def find_recent_duplicate(self, subject: str, window_minutes: int):
        cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
        for ticket in self._tickets:
            if ticket.subject == subject and ticket.created_at >= cutoff:
                return ticket
        return None

    def list_tickets(self):
        return list(self._tickets)

    def create_ticket(self, subject: str, priority: str):
        ticket = Ticket(
            id=self._next_id,
            subject=subject,
            priority=priority,
            created_at=datetime.utcnow(),
        )
        self._tickets.append(ticket)
        self._next_id += 1
        return ticket
