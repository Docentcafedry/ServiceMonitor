import re


def clean_url(url: str) -> str:
    url = re.sub(r"^(https?://)?(www\.)?", "", url)
    return url.rstrip("/")
