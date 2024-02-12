import json
from fastapi import HTTPException, Depends, status

# Load valid API keys from JSON file (replace with your actual storage)
with open("api_keys.json") as f:
    valid_api_keys = set(json.load(f)["keys"])

def validate_api_key(api_key: str):
    if api_key in valid_api_keys:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

# Dependency to get the validated API key
def get_api_key(api_key: str = Depends(validate_api_key)):
    return api_key