def mask_api_key(key: str) -> str:
    key = key.strip()
    if len(key) <= 10:
        return key
    return f"{key[:5]}...{key[-5:]}"
