#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_root="${1:-$repo_root}"
target_root="$repo_root/static/infogest_v2"

required_paths=("index.html" "css" "js" "data")
for rel_path in "${required_paths[@]}"; do
    if [[ ! -e "$source_root/$rel_path" ]]; then
        echo "Missing source path: $source_root/$rel_path" >&2
        exit 1
    fi
done

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

cp -a "$source_root/index.html" "$tmp_dir/index.html"
cp -a "$source_root/css" "$tmp_dir/css"
cp -a "$source_root/js" "$tmp_dir/js"
cp -a "$source_root/data" "$tmp_dir/data"

mkdir -p "$target_root"
rsync -a --delete "$tmp_dir/" "$target_root/"

echo "Synced INFOGEST v2 assets to $target_root"
