def mask_api_key(key: str | None) -> str:
    if key is None:
        return ""
    if not isinstance(key, str):
        raise TypeError(f"mask_api_key expected str | None, got {type(key).__name__}")
    key = key.strip()
    if len(key) <= 10:
        return key
    return f"{key[:5]}...{key[-5:]}"
