from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db.supabase import supabase_client
from app.routes import wishlists, items

app = FastAPI(
    title="REGALOO API",
    description="API per la gestione e creazione di wishlists",
    version="1.0.0")

origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # eventuale altro frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wishlists.router, prefix="/wishlists", tags=["wishlists"])
app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
def root():
    return {"message": "Welcome to REGALOO 🎁"}
    