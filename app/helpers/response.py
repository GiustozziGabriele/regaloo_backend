from datetime import datetime, timezone

def success(function, data=None, is_owner=None):
    return {
        "success": True,
        "data": data,
        "error": None,
        "meta": {
            "function": function,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "is_owner": is_owner
        }
    }

def fail(message, function, code="GENERIC_ERROR"):
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message
        },
        "meta": {
            "function": function,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    }