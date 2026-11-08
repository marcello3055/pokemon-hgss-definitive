#!/usr/bin/env python3
"""Compatibilidade i386 via QEMU, sem alterar código do jogo."""
import argparse,shlex,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(); p.add_argument('source',type=Path); a=p.parse_args()
r=ROOT/'.work/deps/root'; b=a.source.resolve()/'tools/metroskrew/bin'
for path in list(b.iterdir()):
    if path.suffix=='.elf' or path.is_symlink() or not path.is_file(): continue
    if path.read_bytes()[:5]!=b'\x7fELF\x01': continue
    subprocess.run([str(r/'usr/bin/patchelf'),'--set-interpreter',str(r/'usr/lib/i386-linux-gnu/ld-linux.so.2'),'--set-rpath',str(r/'usr/lib/i386-linux-gnu'),str(path)],check=True)
    elf=path.with_name(path.name+'.elf'); path.rename(elf)
    cmd=[str(r/'usr/bin/qemu-i386'),'-0',str(path),str(elf)]
    path.write_text('#!/bin/sh\nexec '+shlex.join(cmd)+' "$@"\n'); path.chmod(0o755)
