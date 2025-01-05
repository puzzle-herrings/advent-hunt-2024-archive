# advent-hunt-2024-archive

Static website archive of the 2024 Advent Puzzle Hunt.

## Generate archive

### Requirements

- `just` — Task runner
- `httrack` — Scraping
- `uv` — Managing Python dependencies and running scripts
- `grep` and `ggrep` - Used for finding missed files


### Steps

1. Scrape the website into the `scraped/` directory
    ```bash
    just scrape
    # or to do a faster version without the team profiles
    just scrape-no-teams
    ```
2. Download files that httrack misses
    ```bash
    just download-missing
    ```
3. Postprocess files into the `publish/` directory
    ```bash
    just postprocess
    ```

## Preview

Preview the website in `publish/` by running `just serve`.
