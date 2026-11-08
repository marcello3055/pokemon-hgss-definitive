#!/usr/bin/env python3
"""Barreira conservadora: somente texto pequeno, sem ROMs/binários/segredos conhecidos."""
import re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ALLOWED={'.md','.py','.sh','.json','.patch','.toml','.txt'}
DENIED={'.nds','.srl','.sav','.dsv','.dst','.nef','.elf','.o','.a','.so','.exe','.deb','.zip','.bundle','.pem','.key'}
PATTERNS=[re.compile(rb'gh[pousr]_[A-Za-z0-9]{30,}'),
          re.compile(rb'github_pat_[A-Za-z0-9_]{40,}'),
          re.compile(rb'-----BEGIN '+rb'(?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]
def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)
def check(path,data):
    p=Path(path)
    if p.suffix.lower() in DENIED or (p.name!='.gitignore' and p.suffix.lower() not in ALLOWED):
        raise ValueError('Arquivo não permitido: '+path)
    if any(x.lower() in ('originals','uploads','assets','bios','credentials','local-deps','.work') for x in p.parts):
        raise ValueError('Diretório não permitido: '+path)
    if len(data)>512000: raise ValueError('Arquivo grande requer revisão: '+path)
    data.decode('utf-8')
    if b'\x00' in data or any(x.search(data) for x in PATTERNS):
        raise ValueError('Possível binário ou segredo: '+path)
def audit():
    files=git('ls-files','-z').decode().split('\0')
    for name in filter(None,files):
        check(name,git('show',':'+name))
        p=ROOT/name
        if p.is_file(): check(name,p.read_bytes())
    objects=0
    if subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=ROOT,capture_output=True).returncode==0:
        for line in git('rev-list','--objects','--all').decode().splitlines():
            oid,_,name=line.partition(' ')
            if git('cat-file','-t',oid).strip()==b'blob':
                check(name,git('cat-file','blob',oid)); objects+=1
    return {'indexed_files':len(list(filter(None,files))),'historical_blobs':objects,'status':'passed'}
if __name__=='__main__':
    import json
    print(json.dumps(audit(),indent=2))
