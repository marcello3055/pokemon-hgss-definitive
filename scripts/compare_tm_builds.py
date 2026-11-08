#!/usr/bin/env python3
"""Check resident-code difference and function layout; result still pending."""
import argparse
import hashlib
import json
from pathlib import Path
from elftools.elf.elffile import ELFFile

def symbols(path):
    with path.open('rb') as f:
        elf = ELFFile(f)
        return {s.name: (int(s['st_value']), int(s['st_size'])) for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name and s['st_info']['type'] == 'STT_FUNC'}

def main():
    p = argparse.ArgumentParser()
    for name in ('baseline_elf','modified_elf','baseline_rom','modified_rom','output'): p.add_argument(name,type=Path)
    a=p.parse_args()
    bs, ms = symbols(a.baseline_elf), symbols(a.modified_elf)
    assert bs == ms, 'function addresses/sizes differ'
    b=a.baseline_elf.with_name('main.sbin').read_bytes(); m=a.modified_elf.with_name('main.sbin').read_bytes()
    assert len(b)==len(m)
    diffs=[(0x02000000+i,x,y) for i,(x,y) in enumerate(zip(b,m)) if x!=y]
    assert len(diffs)==1, diffs[:20]
    addr,old,new=diffs[0]; start,size=bs['PartyMenu_LearnMoveToSlot']; start &= ~1
    assert start<=addr<start+size and (old,new)==(1,0), diffs
    b=a.baseline_rom.read_bytes(); m=a.modified_rom.read_bytes()
    assert len(b)==len(m)==134217728
    assert hashlib.sha1(b).hexdigest()=='4fcded0e2713dc03929845de631d0932ea2b5a37'
    result={'resident_code_differences':[{'address':hex(addr),'before':old,'after':new}], 'function_layout_equal':True,'function_symbols_compared':len(bs),'baseline_sha1':hashlib.sha1(b).hexdigest(),'modified_sha1':hashlib.sha1(m).hexdigest(),'rom_differing_bytes':sum(x!=y for x,y in zip(b,m)),'rom_size':len(b)}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
