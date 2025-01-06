# Print this help documentation
help:
  just --list

url := "https://www.adventhunt.com"
scraped_dir := "scraped/"
publish_dir := "publish/"
exclude_team_profiles := "false"

# Sync Python dependencies
sync:
    uv sync

# Serve the publish/ directory
serve:
    uv run quickhttp publish/

clean-scrape:
    rm -r {{scraped_dir}}

scrape: clean-scrape
    httrack {{url}} \
        -O {{scraped_dir}} \
        '+https://storage.adventhunt.com/*' \
        '+https://cdn.jsdelivr.net/*' \
        '+https://cdnjs.cloudflare.com/*' \
        {{ if exclude_team_profiles == "false" { "" } else { "'-*/teams/*'" } }} \
        -N '%h%p/%n.%t' \
        -K4 # keep original links

scrape-no-teams:
    just exclude_team_profiles=true scrape

download-missing:
    ggrep 'https://storage\.adventhunt\.com[^\s"\)]*' scraped/www.adventhunt.com/ -r --include='*.html' -P -ho \
        | sort -u \
        | SCRAPED_DIR={{ scraped_dir }} xargs -n 1 -P $(nproc) uv run download_missing.py
    ggrep '(?<=["\s])/static/[^"\s]+(?=["\s])'  scraped/www.adventhunt.com/ -r --include='*.html' -P -ho \
        | sort -u \
        | SCRAPED_DIR={{ scraped_dir }} xargs -n 1 -P $(nproc) -I {} uv run download_missing.py "https://www.adventhunt.com{}"

postprocess:
    rm -r {{ publish_dir }}
    SCRAPED_DIR={{ scraped_dir }} PUBLISH_DIR={{ publish_dir }} uv run postprocess.py
