#!/usr/bin/env bash
# Debian x86_64; dependências somente em .work/deps, sem root.
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "$0")/.." && pwd)"
deps_dir="$repo_dir/.work/deps"
mkdir -p "$deps_dir/apt/lists/partial" "$deps_dir/apt/cache/archives/partial" "$deps_dir/root"
cat > "$deps_dir/apt/sources.list" <<'EOF'
deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main
EOF
apt_args=(-o "Dir::Etc::sourcelist=$deps_dir/apt/sources.list" -o Dir::Etc::sourceparts=- -o "Dir::State::lists=$deps_dir/apt/lists" -o "Dir::Cache=$deps_dir/apt/cache" -o APT::Architecture=amd64 -o APT::Architectures::=amd64 -o APT::Architectures::=i386)
apt-get "${apt_args[@]}" update
cd "$deps_dir"
apt-get "${apt_args[@]}" download libc6:i386 libstdc++6:i386 libgcc-s1:i386 bison flex m4 gcc-arm-none-eabi binutils-arm-none-eabi ninja-build nasm libpng-dev libpng16-16t64 zlib1g-dev patchelf qemu-user xdelta3
for package in ./*.deb; do dpkg-deb -x "$package" root; done
sha256sum ./*.deb > packages.sha256
python3 - "$deps_dir" <<'PY'
import shlex,sys
from pathlib import Path
d=Path(sys.argv[1]); r=d/'root'
values={'PKG_CONFIG_PATH':str(r/'usr/lib/x86_64-linux-gnu/pkgconfig'),'PKG_CONFIG_SYSROOT_DIR':str(r),'BISON_PKGDATADIR':str(r/'usr/share/bison'),'M4':str(r/'usr/bin/m4')}
lines=['export PATH='+shlex.quote(str(r/'usr/bin'))+':"$PATH"','export LD_LIBRARY_PATH='+shlex.quote(str(r/'usr/lib/x86_64-linux-gnu'))+'${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}']
lines += ['export '+k+'='+shlex.quote(v) for k,v in values.items()]
lines += ['export PKG_CONFIG_PATH_FOR_BUILD="$PKG_CONFIG_PATH"','export PKG_CONFIG_SYSROOT_DIR_FOR_BUILD="$PKG_CONFIG_SYSROOT_DIR"']
(d/'env.sh').write_text('\n'.join(lines)+'\n')
PY
printf 'Dependências locais preparadas: %s\n' "$deps_dir"
