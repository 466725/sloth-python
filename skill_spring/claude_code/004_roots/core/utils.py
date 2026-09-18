from pathlib import Path
from urllib.parse import unquote, urlparse


def file_url_to_path(file_url) -> Path:
    """Convert a file:// URL to a Path object."""
    url_str = str(file_url)
    parsed = urlparse(url_str)
    path = unquote(parsed.path)
    if len(path) > 2 and path[0] == "/" and path[2] == ":":
        path = path[1:]

    return Path(path)