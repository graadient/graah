#!/bin/sh
# Renders design/social/card.html to public/og-card.png (1200×630).
set -e
cd "$(dirname "$0")"
profile=$(mktemp -d)
google-chrome --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
  --user-data-dir="$profile" --window-size=1200,630 --virtual-time-budget=4000 \
  --screenshot="$PWD/../../public/og-card.png" "file://$PWD/card.html" >/dev/null 2>&1
rm -rf "$profile"
ls -l ../../public/og-card.png
