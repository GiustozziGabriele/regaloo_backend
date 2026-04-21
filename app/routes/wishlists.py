from fastapi import APIRouter
from app.db.supabase import supabase_client

router = APIRouter()

@router.get("/")
def get_wishlists():
    try:
        result = supabase_client.table("wishlists").select("*").execute()
        return result.data

    except Exception as e:
        return str(e)