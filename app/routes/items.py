from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.db.supabase import supabase_client
from app.helpers.auth import get_current_user_id
from app.helpers.response import *
from app.models.items import Item, ItemCreate, AddExistingItems
from app.models.item_context import ItemContext, ItemContextCreate

router = APIRouter()

@router.post("/{wishlist_id}/create-item")
def create_wishlist_item(payload: ItemCreate, wishlist_id: str, user_id: str = Depends(get_current_user_id)):
    item = Item.from_create(payload, user_id)
    function_name = 'create_wishlist_item'

    try:
        item_result = supabase_client.table('items').insert(item.to_dict()).execute()
        if not item_result.data:
            return JSONResponse(
                status_code=400,
                content=fail(message="Errore durante la creazione dell'item", function=function_name, code="ITEM_CREATE_FAILED")
            )
        
        item = Item(item_result.data[0])
        item_context = ItemContextCreate(item_id=item.id, created_by_user_id=user_id, wishlist_id=wishlist_id)

        item_context_result = supabase_client.table('item_context').insert(item_context.model_dump()).execute()
        if not item_context_result.data:
            supabase_client.table('items').delete().eq('id', item.id).execute()
            return JSONResponse(
                status_code=400,
                content=fail(message="Errore durante la creazione dell'item_context", function=function_name, code="ITEM_CONTEXT_CREATE_FAILED")
            )
        
        item_context_object = ItemContext(item_context_result.data[0])
        
        
        return JSONResponse(
            status_code=200,
            content=success(function=function_name, data=item_context_object.to_response(item))
        )

    except Exception as e: 
        return JSONResponse(
            status_code=500,
            content=fail(message="Errore interno del server", function=function_name, code="INTERNAL_ERROR")
        )

@router.get("/{wishlist_id}/available")
def get_available_items(wishlist_id: str, user_id: str = Depends(get_current_user_id)):
    function_name = 'get_available_items'

    try:
        # 1. prendi item già nella wishlist
        used = supabase_client \
            .table('item_context') \
            .select('item_id') \
            .eq('wishlist_id', wishlist_id) \
            .execute()

        used_ids = [i['item_id'] for i in used.data] if used.data else []

        # 2. query items NON usati
        query = supabase_client \
            .table('items') \
            .select('*') \
            .eq('user_id', user_id)

        if used_ids:
            query = query.not_.in_('id', used_ids)

        result = query.execute()

        return JSONResponse(
            status_code=200,
            content=success(data=result.data, function=function_name)
        ) 

    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content=fail(message="Errore recupero items disponibili", function=function_name, code="INTERNAL_ERROR")
        )
    
@router.post("/{wishlist_id}/add-existing")
def add_existing_items(wishlist_id: str, payload: AddExistingItems, user_id: str = Depends(get_current_user_id)):
    function_name = 'add_existing_items'

    try:
        contexts = [
            ItemContextCreate(
                item_id=item_id,
                created_by_user_id=user_id,
                wishlist_id=wishlist_id
            ).model_dump()
            for item_id in payload.item_ids
        ]

        result = supabase_client.table('item_context').insert(contexts).execute()

        if not result.data:
            return JSONResponse(
                status_code=400,
                content=fail(message="Errore durante l'aggiunta degli articoli", function=function_name, code="ITEM_CONTEXT_CREATE_FAILED")
            )

        # fetch con join per avere item_id(*) come nel fetchWishlistItems
        ids = [row['id'] for row in result.data]
        enriched = supabase_client.table('item_context') \
            .select('*, item_id(*)') \
            .in_('id', ids) \
            .execute()

        return JSONResponse(
            status_code=200,
            content=success(function=function_name, data=enriched.data)
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=fail(message="Errore interno del server", function=function_name, code="INTERNAL_ERROR")
        )