#!/usr/bin/env python3
"""Compile a minimal registry-engine consumer outside ancestor Cargo patches."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = ROOT/'target/consumer-check'/uuid.uuid4().hex
    output.mkdir(parents=True)
    before = hashlib.sha256((ROOT/'Cargo.lock').read_bytes()).hexdigest() if (ROOT/'Cargo.lock').exists() else None
    with tempfile.TemporaryDirectory(prefix='inspector consumer ') as temporary:
        source = Path(temporary)
        (source/'src').mkdir()
        manifest = ('[package]\nname="inspector-consumer"\nversion="0.0.0"\nedition="2024"\n'
                    '[workspace]\n[dependencies]\nbevy-inspector-egui={path='
                    + json.dumps(str(ROOT/'crates/bevy-inspector-egui')) + ',default-features=false}\n')
        (source/'Cargo.toml').write_text(manifest)
        (source/'src/main.rs').write_text('fn main() { let _ = bevy_inspector_egui::inspector_options::InspectorOptions::default(); }\n')
        report = {'scope':'standalone no-default consumer; not a rendered UI qualification',
                  'manifest':manifest, 'status':'RUNNING', 'commands':[]}
        (output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
        for index, command in enumerate([
            ['cargo','check','--offline','--target-dir',str(ROOT/'target/consumer-cargo')],
            ['cargo','metadata','--offline','--format-version','1'],
        ]):
            result = subprocess.run(command, cwd=source, env=dict(os.environ, CARGO_INCREMENTAL='0'), capture_output=True, text=True)
            (output/f'command-{index}.stdout').write_text(result.stdout)
            (output/f'command-{index}.stderr').write_text(result.stderr)
            report['commands'].append({'command':command, 'exit_code':result.returncode})
            if result.returncode:
                report['status'] = 'FAIL'
                break
        else:
            metadata = json.loads(result.stdout)
            engines = [p for p in metadata['packages'] if p['name'].startswith('bevy') and not p['name'].startswith('bevy-inspector-egui')]
            report['engines'] = [{'name':p['name'], 'version':p['version'], 'source':p['source']} for p in engines]
            report['status'] = 'PASS' if all((p['source'] or '').startswith('registry+') for p in engines) else 'FAIL'
            report['resolved_lock_sha256'] = hashlib.sha256((source/'Cargo.lock').read_bytes()).hexdigest()
    after = hashlib.sha256((ROOT/'Cargo.lock').read_bytes()).hexdigest() if (ROOT/'Cargo.lock').exists() else None
    report.update(checkout_lock_before=before, checkout_lock_after=after)
    if before != after:
        report['status'] = 'FAIL'
    (output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(f"{report['status']}: {output/'report.json'}")
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
