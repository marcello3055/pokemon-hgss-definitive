#!/usr/bin/env python3
"""Run existing TM checks in small stages and retain an atomic, sanitized report.

Does not build ROMs or declare UI/save validation complete. Local reports must
be copied to the authorized Git repository after inspection.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['preflight', 'binary', 'arm', 'boot'])
    args = parser.parse_args()
    dest = ROOT / 'artifacts/tm-wip'
    dest.mkdir(parents=True, exist_ok=True)
    report_path = dest / ('validation-' + args.stage + '.json')
    base = ROOT / '.work/baseline/build/heartgold.us/main.nef'
    mod = ROOT / '.work/tm-wip/build/heartgold.us/main.nef'
    base_rom = ROOT / 'artifacts/baseline/heartgold.nds'
    mod_rom = dest / 'heartgold.nds'
    required = {
        'preflight': [base, mod, base.with_name('main.sbin'), mod.with_name('main.sbin'), base_rom, mod_rom],
        'binary': [base, mod, base.with_name('main.sbin'), mod.with_name('main.sbin'), base_rom, mod_rom],
        'arm': [base, mod, base.with_name('main.sbin'), mod.with_name('main.sbin')],
        'boot': [mod_rom],
    }[args.stage]
    report = {'stage': args.stage, 'time_utc': datetime.now(timezone.utc).isoformat(),
              'status': 'started', 'ui_and_save_validation': 'pending'}
    def save():
        temp = report_path.with_suffix('.tmp')
        temp.write_text(json.dumps(report, indent=2) + '\n')
        temp.replace(report_path)
    save()
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    if missing:
        report.update(status='blocked', missing=missing)
        save()
        print(json.dumps(report, indent=2))
        return 2
    commands = {
        'binary': ['compare_tm_builds.py', base, mod, base_rom, mod_rom, dest / 'binary-comparison.json'],
        'arm': ['test_tm_arm.py', base, mod, dest / 'arm-tests.json'],
        'boot': ['boot_smoke.py', mod_rom, dest / 'title.png'],
    }
    if args.stage == 'preflight':
        report['status'] = 'inputs_present_not_validated'
    else:
        cmd = commands[args.stage]
        env = os.environ.copy()
        env['PYTHONPATH'] = str(ROOT / '.work/python')
        # Logs stay local: never copy an unreviewed environment dump to GitHub.
        with (dest / ('validation-' + args.stage + '.log')).open('w') as log:
            run = subprocess.run([sys.executable, str(ROOT / 'scripts' / cmd[0]), *map(str, cmd[1:])], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
        report.update(returncode=run.returncode, status='passed' if run.returncode == 0 else 'failed')
        if args.stage == 'boot' and run.returncode == 0:
            report['status'] = 'frames_completed_image_review_pending'
    save()
    print(json.dumps(report, indent=2))
    return 1 if report['status'] == 'failed' else 0

if __name__ == '__main__':
    raise SystemExit(main())
