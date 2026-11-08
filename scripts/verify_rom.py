#!/usr/bin/env python3
"""Verifica HeartGold US sem alterar o arquivo fornecido."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

EXPECTED = "4fcded0e2713dc03929845de631d0932ea2b5a37"

def sha1(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha1").hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path)
    parser.add_argument("--backup-dir", type=Path)
    args = parser.parse_args()
    digest = sha1(args.rom)
    result = {"filename": args.rom.name, "bytes": args.rom.stat().st_size,
              "sha1": digest, "expected_sha1": EXPECTED, "matches": digest == EXPECTED}
    print(json.dumps(result, indent=2))
    if digest != EXPECTED:
        raise SystemExit("ROM diferente da base esperada; nenhuma copia criada.")
    if args.backup_dir:
        args.backup_dir.mkdir(parents=True, exist_ok=True)
        dest = args.backup_dir / "heartgold-us-original.nds"
        # Exclusive creation prevents replacing an earlier original.
        with args.rom.open("rb") as src, dest.open("xb") as dst:
            shutil.copyfileobj(src, dst)
        if sha1(dest) != EXPECTED:
            raise SystemExit("Falha na verificacao da copia; nao utilizar.")
        dest.chmod(0o444)
        print("Copia original verificada e marcada somente para leitura:", dest)

if __name__ == "__main__":
    main()
