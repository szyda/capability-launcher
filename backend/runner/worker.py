#!/usr/bin/env python3
import importlib.util
import json
import sys
from pathlib import Path


def load_capability_module(capability_dir: Path):
    main_path = capability_dir / 'main.py'
    if not main_path.exists():
        raise FileNotFoundError(f'Missing entry point: {main_path}')

    spec = importlib.util.spec_from_file_location('capability_main', main_path)
    if spec is None or spec.loader is None:
        raise ImportError(f'Could not load module from {main_path}')

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    if len(sys.argv) < 3:
        print(json.dumps({'ok': False, 'error': 'Capability directory and inputs are required.'}))
        raise SystemExit(2)

    capability_dir = Path(sys.argv[1]).resolve()
    payload = json.loads(sys.argv[2])

    try:
        module = load_capability_module(capability_dir)
        run_fn = getattr(module, 'run', None)
        if run_fn is None or not callable(run_fn):
            raise ValueError('Capability entry point must define a callable run(inputs)')

        result = run_fn(payload)
        if not isinstance(result, dict):
            raise TypeError('Capability output must be a JSON-compatible dictionary.')

        print(json.dumps({'ok': True, 'result': result}))
        raise SystemExit(0)
    except Exception as exc:  # pragma: no cover - worker side failure
        print(json.dumps({'ok': False, 'error': str(exc)}))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
