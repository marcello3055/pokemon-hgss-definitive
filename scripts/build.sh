#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "$0")/.." && pwd)"
variant="${1:-}"
case "$variant" in baseline|tm-wip) ;; *) echo 'Uso: build.sh baseline|tm-wip' >&2; exit 2;; esac
source "$repo_dir/.work/deps/env.sh"
# Meson expects NINJA to name an executable, not a command with arguments.
mkdir -p "$repo_dir/.work/bin"
cat > "$repo_dir/.work/bin/ninja-limited" <<EOF
#!/usr/bin/env bash
exec "$repo_dir/.work/deps/root/usr/bin/ninja" -j4 "\$@"
EOF
chmod +x "$repo_dir/.work/bin/ninja-limited"
export NINJA="$repo_dir/.work/bin/ninja-limited"
python3 "$repo_dir/scripts/prepare_source.py" "$variant"
source_dir="$repo_dir/.work/$variant"
mkdir -p "$repo_dir/artifacts/$variant"
make -C "$source_dir" skrew meson
python3 "$repo_dir/scripts/wrap_toolchain.py" "$source_dir"
if [[ "$variant" == baseline ]]; then
    make -C "$source_dir" 2>&1 | tee "$repo_dir/artifacts/$variant/build.log"
else
    make -C "$source_dir" rom 2>&1 | tee "$repo_dir/artifacts/$variant/build.log"
fi
cp "$source_dir/build/heartgold.us/pokeheartgold.us.nds" "$repo_dir/artifacts/$variant/heartgold.nds"
sha1sum "$repo_dir/artifacts/$variant/heartgold.nds" | tee "$repo_dir/artifacts/$variant/rom.sha1"
if [[ "$variant" == baseline ]]; then
    python3 "$repo_dir/scripts/verify_rom.py" "$repo_dir/artifacts/$variant/heartgold.nds"
fi
