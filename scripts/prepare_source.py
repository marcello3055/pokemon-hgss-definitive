#!/usr/bin/env python3
"""Recupera a base fixa fora do histórico próprio."""
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(*args,cwd=None):
    return subprocess.check_output(args,cwd=cwd,text=True).strip()
def main():
    p=argparse.ArgumentParser(); p.add_argument('variant',choices=['baseline','tm-wip']); a=p.parse_args()
    lock=json.loads((ROOT/'upstream.lock.json').read_text()); dest=ROOT/'.work'/a.variant
    if not (dest/'.git').exists():
        dest.mkdir(parents=True,exist_ok=True)
        run('git','init',str(dest))
        run('git','remote','add','origin',lock['repository'],cwd=dest)
        run('git','fetch','--depth','1','origin',lock['commit'],cwd=dest)
        run('git','checkout','--detach',lock['commit'],cwd=dest)
    if run('git','rev-parse','HEAD',cwd=dest)!=lock['commit']:
        raise SystemExit('Revisão divergente: interrompido sem apagar alterações.')
    if a.variant=='tm-wip':
        patch=ROOT/'patches/0001-infinite-tms-WIP.patch'
        reverse=subprocess.run(['git','apply','--reverse','--check',str(patch)],cwd=dest,capture_output=True)
        if reverse.returncode:
            run('git','apply','--check',str(patch),cwd=dest)
            run('git','apply',str(patch),cwd=dest)
    print(dest)
if __name__=='__main__': main()
