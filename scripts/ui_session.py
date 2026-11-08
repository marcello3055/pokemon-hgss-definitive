#!/usr/bin/env python3
"""Private manual QA console. Run with python3 -i; never use a player save."""
import hashlib
import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
from desmume.emulator import DeSmuME
from desmume.controls import Keys, keymask

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "artifacts/ui-test"
ROM = QA / "test.nds"
assert hashlib.sha1(ROM.read_bytes()).hexdigest() == "34f3068802d836309eeb6da01460f9e32b26ad4d", "Wrong QA ROM"
e = DeSmuME()
e.volume_set(0)
e.open(str(ROM))
if (QA / "latest.dst").exists():
    e.savestate.load_file(str(QA / "latest.dst"))

def frames(n):
    for _ in range(n):
        e.cycle(with_joystick=False)

def key(k, n=8, after=160):
    e.input.keypad_add_key(keymask(k))
    frames(n)
    e.input.keypad_rm_key(keymask(k))
    frames(after)

def tap(x, y, after=160):
    e.input.touch_set_pos(x, y)
    frames(8)
    e.input.touch_release()
    frames(after)

def shot():
    e.screenshot().save(str(QA / "live.png"))
    e.savestate.save_file(str(QA / "latest.dst"))

def tm_pocket():
    """Addresses verified against the pinned build; this console checks its hash."""
    save = e.memory.unsigned.read_long(0x021D2228)
    assert 0x02000000 <= save < 0x02400000
    header = save + 0x23014 + 3 * 16
    assert e.memory.unsigned.read_long(header) == 3
    bag = save + 16 + e.memory.unsigned.read_long(header + 8)
    return bag + 860

def seed_protect():
    """Call ONLY in overworld, with empty TM pocket, for private QA."""
    ptr = tm_pocket()
    assert all(e.memory.unsigned.read_short(ptr + i * 2) == 0 for i in range(202)), "TM pocket is not empty"
    e.memory.write_short(ptr, 344)
    e.memory.write_short(ptr + 2, 1)

def export_save():
    """Call after normal in-game save has finished. This does not save the game."""
    assert e.backup.export_file(str(QA / "test.sav")), "Backup export failed"
    assert (QA / "test.sav").stat().st_size == 524288

shot()
print("QA console ready: frames(n), key(Keys.KEY_A), tap(x,y), shot().")
