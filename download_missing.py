import os
from pathlib import Path
from urllib.parse import urlparse

from cyclopts import App
import httpx
from loguru import logger

app = App()

SCRAPED_DIR = Path(os.environ.get("SCRAPED_DIR"))


@app.default
def main(url: str):
    parsed_url = urlparse(url)
    out_path = SCRAPED_DIR / parsed_url.netloc / Path(parsed_url.path.removeprefix("/"))
    logger.info(f"Downloading {url} to {out_path} ...")
    try:
        response = httpx.get(url)
        response.raise_for_status()
        with out_path.open("wb") as fp:
            fp.write(response.content)
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")


app()
