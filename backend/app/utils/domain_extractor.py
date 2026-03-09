from urllib.parse import urlparse


def extract_domain(referer: str | None, origin: str | None) -> str | None:
    for header in (referer, origin):
        if header:
            parsed = urlparse(header)
            if parsed.netloc:
                return parsed.netloc
    return None
