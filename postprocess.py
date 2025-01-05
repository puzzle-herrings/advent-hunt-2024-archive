import os
from pathlib import Path
import re
import shutil

from loguru import logger
from tqdm import tqdm

SCRAPED_DIR = Path(os.environ.get("SCRAPED_DIR"))
PUBLISH_DIR = Path(os.environ.get("PUBLISH_DIR"))

EXCLUDE_FILES = {
    ".DS_Store",
}

REGEX_SUBSTITUTIONS = (
    (re.compile(r"(\.\./)+cdn\.jsdelivr\.net"), "/libraries/jsdelivr"),
    (re.compile(r"(\.\./)+cdnjs\.cloudflare\.com"), "/libraries/cdnjs"),
    (re.compile(r"(\.\./)+storage\.adventhunt\.com"), "/storage"),
    (re.compile(r"https://storage\.adventhunt\.com"), "/storage"),
)

EXTERNAL_DIRECTORY_MAP = (
    ("cdn.jsdelivr.net", "libraries/jsdelivr"),
    ("cdnjs.cloudflare.com", "libraries/cdnjs"),
    ("storage.adventhunt.com", "storage"),
)


def process_content(content: str):
    for regex, replacement in REGEX_SUBSTITUTIONS:
        content = regex.sub(replacement, content)
    return content


def move_file(in_path: Path, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if in_path.suffix == ".html":
        with in_path.open("r") as fr, out_path.open("w") as fw:
            content = fr.read()
            fw.write(process_content(content))
    else:
        shutil.copy(in_path, out_path)


def main():
    # Move main website files
    logger.info("Moving main website files ...")
    for path in tqdm(sorted((SCRAPED_DIR / "www.adventhunt.com").glob("**/*"))):
        if not path.is_file():
            continue
        if path.name in EXCLUDE_FILES:
            continue
        out_path = PUBLISH_DIR / path.relative_to(SCRAPED_DIR / "www.adventhunt.com")
        move_file(path, out_path)

    # Move external website files
    for external_dirname, out_dirname in EXTERNAL_DIRECTORY_MAP:
        logger.info("Moving external website files from {} ...", external_dirname)
        for path in tqdm(sorted((SCRAPED_DIR / external_dirname).glob("**/*"))):
            if not path.is_file():
                continue
            if path.name in EXCLUDE_FILES:
                continue
            out_path = (
                PUBLISH_DIR / Path(out_dirname) / path.relative_to(SCRAPED_DIR / external_dirname)
            )
            move_file(path, out_path)


if __name__ == "__main__":
    main()
