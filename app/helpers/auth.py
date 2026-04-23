from fastapi import Request, HTTPException
from app.db.supabase import supabase_client

def get_current_user_id(request: Request) -> str:
    auth_header = request.headers.get("authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        token = auth_header.split(" ")[1]
        user = supabase_client.auth.get_user(token)

        return user.user.id

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_optional_user_id():
    try:
        return get_current_user_id()
    except:
        return None