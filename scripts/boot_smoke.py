#!/usr/bin/env python3
"""Abertura automatizada. Não valida campanha nem TMs."""
import argparse,os
from pathlib import Path
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
from desmume.emulator import DeSmuME
from desmume.controls import Keys,keymask
p=argparse.ArgumentParser(); p.add_argument('rom'); p.add_argument('image',type=Path); a=p.parse_args()
a.image.parent.mkdir(parents=True,exist_ok=True)
e=DeSmuME(); e.volume_set(0)
try:
    e.open(a.rom)
    for frame in range(1800):
        if frame==650: e.input.keypad_add_key(keymask(Keys.KEY_START))
        if frame==655: e.input.keypad_rm_key(keymask(Keys.KEY_START))
        e.cycle(with_joystick=False)
    e.screenshot().save(str(a.image))
    print('1800 frames executados; examinar imagem antes de declarar aprovação.')
finally:
    e.destroy()
