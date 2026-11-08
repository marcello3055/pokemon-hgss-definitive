#!/usr/bin/env python3
"""Cria backup Git e comprova restauração antes de empacotar."""
import argparse,io,json,subprocess,tempfile,zipfile,hashlib
from pathlib import Path
from audit_repo import audit,ROOT
def git(*args,cwd=ROOT):
    return subprocess.check_output(['git',*map(str,args)],cwd=cwd).decode().strip()
p=argparse.ArgumentParser(); p.add_argument('output',type=Path); a=p.parse_args()
dest=a.output.resolve()
if dest.is_relative_to(ROOT): raise SystemExit('Salvar checkpoint fora do repositório.')
if dest.exists(): raise SystemExit('Destino já existe; usar novo nome de checkpoint.')
if git('status','--porcelain'): raise SystemExit('Árvore não está limpa; registrar alterações antes.')
report=audit(); head=git('rev-parse','HEAD')
with tempfile.TemporaryDirectory() as d:
    d=Path(d); bundle=d/'hgss-definitive.bundle'
    git('bundle','create',bundle,'--all')
    git('bundle','verify',bundle)
    clone=d/'restore'
    git('clone',bundle,clone,cwd=d)
    assert git('rev-parse','HEAD',cwd=clone)==head
    assert not git('status','--porcelain',cwd=clone)
    git('fsck','--full',cwd=clone)
    # Confirm identical tracked tree, not merely matching ref.
    assert git('ls-tree','-r','HEAD',cwd=clone)==git('ls-tree','-r','HEAD')
    archive=subprocess.check_output(['git','archive','--format=zip','HEAD'],cwd=ROOT)
    report.update(commit=head,bundle_sha256=hashlib.sha256(bundle.read_bytes()).hexdigest(),
                  restore_test='passed',source_tree_test='passed',
                  note='Backup local verificado; ainda requer salvar em destino persistente.')
    dest.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(dest,'x',zipfile.ZIP_DEFLATED) as z:
        z.write(bundle,bundle.name)
        z.writestr('CHECKPOINT.json',json.dumps(report,indent=2)+'\n')
        z.writestr('RESTORE.txt','Para o agente: git clone hgss-definitive.bundle hgss-definitive\nLer PROGRESS.md antes de continuar.\n')
        with zipfile.ZipFile(io.BytesIO(archive)) as source:
            for item in source.infolist(): z.writestr('source/'+item.filename,source.read(item))
print(json.dumps(report,indent=2)); print(dest)
