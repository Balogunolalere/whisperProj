# api_keys.py
from fastapi import APIRouter, HTTPException, status
import secrets
import json
from ..utils.validations import validate_api_key, valid_api_keys

router = APIRouter()

@router.post("/create_api_key")
async def create_api_key():
    new_key = secrets.token_urlsafe(32)  # Generate a new key
    valid_api_keys.add(new_key)  # Add the new key to the set of valid keys

    # Write the updated set of keys back to the JSON file
    with open("api_keys.json", "w") as f:
        json.dump({"keys": list(valid_api_keys)}, f)

    return {"api_key": new_key}

@router.delete("/revoke_api_key")
async def revoke_api_key(api_key: str):
    if api_key in valid_api_keys:
        valid_api_keys.remove(api_key)  # Remove the key from the set of valid keys

        # Write the updated set of keys back to the JSON file
        with open("api_keys.json", "w") as f:
            json.dump({"keys": list(valid_api_keys)}, f)

        return {"detail": "API key revoked"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )

@router.get("/validate_api_key")
async def validate_key(api_key: str):
    key = validate_api_key(api_key)
    # If the key is valid, the function will return True else it will raise an exception
    if key:
        return {"detail": "API key is valid"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
