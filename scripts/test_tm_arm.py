#!/usr/bin/env python3
"""Compiled learning + real Bag_TakeItem; external services mocked, no UI/save coverage."""
import argparse
import json
import struct
from pathlib import Path
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_SP

def test(elf_path, infinite):
    emu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    emu.mem_map(0x02000000, 0x400000)
    with open(elf_path, 'rb') as f:
        elf = ELFFile(f)
        symbols = {s.name: int(s['st_value']) for s in elf.get_section_by_name('.symtab').iter_symbols()}
    # NEF contains symbols, but resident executable bytes live in main.sbin.
    emu.mem_write(0x02000000, Path(elf_path).with_name('main.sbin').read_bytes())
    menu, args, bag, mon, stop = 0x02380000, 0x02381000, 0x02382000, 0x02384000, 0x023f0000
    writes, effects, takes = [], [], []
    def u32(addr): return struct.unpack('<I', emu.mem_read(addr, 4))[0]
    def put(addr, fmt, *values): emu.mem_write(addr, struct.pack(fmt, *values))
    def reg(n): return emu.reg_read(n)
    def ret(value=0):
        emu.reg_write(UC_ARM_REG_R0, value)
        emu.reg_write(UC_ARM_REG_PC, reg(UC_ARM_REG_LR))
    hooks = {symbols[n] & ~1: n for n in ['SetMonData', 'GetMoveMaxPP', 'MoveIsHM', 'GetItemAttr', 'PartyMenu_GetCurrentMapSec', 'MonApplyFriendshipMod', 'ApplyMonMoodModifier', 'Bag_TakeItem']}
    def callback(uc, address, size, unused):
        name = hooks.get(address)
        if name == 'SetMonData':
            writes.append((reg(UC_ARM_REG_R1), u32(reg(UC_ARM_REG_R2)))); ret()
        elif name == 'GetMoveMaxPP': ret(10)
        elif name == 'MoveIsHM': ret(int(reg(UC_ARM_REG_R0) == 15))
        elif name == 'GetItemAttr': ret(3)
        elif name == 'PartyMenu_GetCurrentMapSec': ret(1)
        elif name in ('MonApplyFriendshipMod', 'ApplyMonMoodModifier'):
            effects.append(name); ret()
        elif name == 'Bag_TakeItem': takes.append(reg(UC_ARM_REG_R2))
    emu.hook_add(UC_HOOK_CODE, callback)
    put(menu + 0x654, '<I', args)
    put(args + 4, '<I', bag)
    results = []
    def learn(slot, item=344, move=182):
        writes.clear(); effects.clear(); takes.clear()
        put(args + 0x28, '<HH', item, move)
        for register, value in [(UC_ARM_REG_R0, menu), (UC_ARM_REG_R1, mon), (UC_ARM_REG_R2, slot), (UC_ARM_REG_SP, 0x023ff000), (UC_ARM_REG_LR, stop | 1)]:
            emu.reg_write(register, value)
        emu.emu_start(symbols['PartyMenu_LearnMoveToSlot'] | 1, stop, count=1000000)
        assert reg(UC_ARM_REG_PC) == stop, 'routine did not return'
        assert writes == [(54 + slot, move), (62 + slot, 0), (58 + slot, 10)], writes
    for quantity in (1, 2, 99):
        for slot in range(4):
            emu.mem_write(bag, bytes(4096))
            put(bag + 860, '<HHHH', 344, quantity, 345, 7)
            learn(slot)
            first = struct.unpack('<HH', emu.mem_read(bag + 860, 4))
            expected = (344, quantity) if infinite else ((344, quantity-1) if quantity>1 else (345, 7))
            assert first == expected, (first, expected)
            assert takes == [0 if infinite else 1], takes
            assert len(effects) == 2
            results.append({'quantity': quantity, 'slot': slot, 'passed': True})
    if infinite:
        emu.mem_write(bag, bytes(4096)); put(bag + 860, '<HH', 344, 1)
        for _ in range(20): learn(0)
        assert struct.unpack('<HH', emu.mem_read(bag + 860, 4)) == (344, 1)
    emu.mem_write(bag, bytes(4096)); put(bag + 860, '<HH', 420, 1)
    learn(0, 420, 15)
    assert not takes and len(effects) == 2
    assert struct.unpack('<HH', emu.mem_read(bag + 860, 4)) == (420, 1)
    learn(0, 0, 182)
    assert not takes and not effects
    return {'elf': str(elf_path), 'infinite': infinite, 'cases': results, 'hm_preserved': True, 'no_item_preserved': True, 'repeated_20': infinite, 'limitations': 'External Pokemon/PP/metadata/friendship services mocked; no UI or save coverage.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('baseline'); p.add_argument('modified'); p.add_argument('output', type=Path); a = p.parse_args()
    result = {'baseline': test(a.baseline, False), 'modified': test(a.modified, True)}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2) + '\n')
    print('Compiled ARM learning/bag tests passed for baseline and modified build.')
