#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "$0")/.." && pwd)"
variant="${1:-}"
case "$variant" in baseline|tm-wip) ;; *) echo 'Uso: build.sh baseline|tm-wip' >&2; exit 2;; esac
source "$repo_dir/.work/deps/env.sh"
python3 "$repo_dir/scripts/prepare_source.py" "$variant"
source_dir="$repo_dir/.work/$variant"
mkdir -p "$repo_dir/artifacts/$variant"
make -C "$source_dir" skrew meson
python3 "$repo_dir/scripts/wrap_toolchain.py" "$source_dir"
if [[ "$variant" == baseline ]]; then
    make -C "$source_dir" NINJA='ninja -j4' 2>&1 | tee "$repo_dir/artifacts/$variant/build.log"
else
    make -C "$source_dir" rom NINJA='ninja -j4' 2>&1 | tee "$repo_dir/artifacts/$variant/build.log"
fi
cp "$source_dir/build/heartgold.us/pokeheartgold.us.nds" "$repo_dir/artifacts/$variant/heartgold.nds"
sha1sum "$repo_dir/artifacts/$variant/heartgold.nds" | tee "$repo_dir/artifacts/$variant/rom.sha1"
if [[ "$variant" == baseline ]]; then
    python3 "$repo_dir/scripts/verify_rom.py" "$repo_dir/artifacts/$variant/heartgold.nds"
fi
