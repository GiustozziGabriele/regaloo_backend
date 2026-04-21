from pydantic import BaseModel
from datetime import datetime
from fastapi import HTTPException
from app.models.items import Item

class ItemContextCreate(BaseModel):
    item_id: str 
    created_by_user_id: str 
    wishlist_id: str | None = None
    event_id: str | None = None
    status: str | None = 'available'
    reserved_by_user_id: str | None = None
    purchased_at: str | None = None
    delivered_at: str | None = None

class ItemContextResponse(BaseModel):
    id: str
    item_id: str 
    created_by_user_id: str 
    wishlist_id: str | None = None
    event_id: str | None = None
    status: str 
    reserved_by_user_id: str | None = None
    purchased_at: str | None = None
    delivered_at: str | None = None
    created_at: datetime

class UpdateItemContext(BaseModel):
    status: str | None = None
    reserved_by_user_id: str | None = None
    purchased_at: datetime | None = None
    delivered_at: datetime | None = None


# --- CLASSE DI DOMINIO con logica ---

class ItemContext:
    def __init__(self, data: dict):
        self.id = data.get('id')
        self.item_id = data.get('item_id')
        self.created_by_user_id = data.get('created_by_user_id')
        self.wishlist_id = data.get('wishlist_id')
        self.event_id = data.get('event_id')
        self.status = data.get('status', 'available')
        self.reserved_by_user_id = data.get('reserved_by_user_id')
        self.purchased_at = data.get('purchased_at')
        self.delivered_at = data.get('delivered_at')
        self.created_at = data.get('created_at')

    @classmethod
    def from_create(cls, data: ItemContextCreate):
        return cls({
            "item_id": data.item_id,
            "created_by_user_id": data.created_by_user_id,
            "wishlist_id": data.wishlist_id,
            "event_id": data.event_id,
            "status": data.status or "available",
            "reserved_by_user_id": data.reserved_by_user_id,
            "purchased_at": data.purchased_at,
            "delivered_at": data.delivered_at
        })
    
    def to_response(self, item: Item):
        return {
            "id": self.id,
            "item_id": item.to_dict(),  # 👈 join qui
            "created_by_user_id": self.created_by_user_id,
            "wishlist_id": self.wishlist_id,
            "event_id": self.event_id,
            "status": self.status,
            "reserved_by_user_id": self.reserved_by_user_id,
            "purchased_at": self.purchased_at,
            "delivered_at": self.delivered_at,
            "created_at": self.created_at
        }

    def to_dict(self):
        data = {
            "item_id": self.item_id,
            "created_by_user_id": self.created_by_user_id,
            "status": self.status
        }

        # SOLO se esiste davvero (lettura DB)
        if self.id is not None:
            data["id"] = self.id

        if self.created_at is not None:
            data["created_at"] = self.created_at

        if self.delivered_at is not None:
            data["delivered_at"] = self.delivered_at

        if self.purchased_at is not None:
            data["purchased_at"] = self.purchased_at

        if self.reserved_by_user_id is not None:
            data["reserved_by_user_id"] = self.reserved_by_user_id

        if self.wishlist_id is not None:
            data["wishlist_id"] = self.wishlist_id

        if self.event_id is not None:
            data["event_id"] = self.event_id

        return data