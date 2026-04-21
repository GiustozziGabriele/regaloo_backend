from pydantic import BaseModel
from datetime import datetime
from fastapi import HTTPException

class ItemCreate(BaseModel):
    title: str
    url: str | None = None
    price: float | None = None
    image_url: str | None = None

class ItemResponse(BaseModel):
    id: str
    user_id: str
    title: str
    url: str | None
    image_url: str | None = None
    price: float | None
    created_at: datetime


# --- CLASSE DI DOMINIO con logica ---

class Item:
    def __init__(self, data: dict):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.title = data.get('title')
        self.url = data.get('url')
        self.image_url = data.get('image_url')
        self.price = data.get('price')
        self.created_at = data.get('created_at')

    @classmethod
    def from_create(cls, data: ItemCreate, user_id: str):
        return cls({
            "user_id": user_id,   # 👈 SEMPRE qui
            "title": data.title,
            "url": data.url,
            "image_url": data.image_url,
            "price": data.price
        })

    def to_dict(self):
        data = {
            "user_id": self.user_id,
            "title": self.title,
            "url": self.url,
            "image_url": self.image_url,
            "price": self.price
        }

        # SOLO se esiste davvero (lettura DB)
        if self.id is not None:
            data["id"] = self.id

        if self.created_at is not None:
            data["created_at"] = self.created_at

        return data