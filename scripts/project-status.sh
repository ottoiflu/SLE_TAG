#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

repo_status() {
    local label="$1"
    local path="$2"

    printf '\n== %s ==\n' "$label"
    if [ -d "$path/.git" ] || git -C "$path" rev-parse --git-dir >/dev/null 2>&1; then
        git -C "$path" status --short --branch
    else
        printf 'not a Git repository: %s\n' "$path"
    fi
}

repo_status "project root" "$ROOT"
repo_status "firmware: sle_local" "$ROOT/sle_local"
repo_status "flasher: hisiflash" "$ROOT/hisiflash"

printf '\n== key artifacts ==\n'
for file in \
    "$ROOT/sle_local/src/output/bs21e/fwpkg/standard-bs21e-1100e/bs21e_all_in_one.fwpkg" \
    "$ROOT/hisiflash/target/release/hisiflash"; do
    if [ -f "$file" ]; then
        stat --printf='%y  %s bytes  %n\n' "$file"
    else
        printf 'missing: %s\n' "$file"
    fi
done

printf '\n== disk usage ==\n'
du -sh "$ROOT/Docs" "$ROOT/sle_local" "$ROOT/hisiflash" 2>/dev/null
