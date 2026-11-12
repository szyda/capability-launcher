#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CAPABILITIES_DIR = ROOT / 'capabilities'


def ensure_venv(capability_dir: Path) -> Path:
    venv_dir = capability_dir / '.venv'
    if not venv_dir.exists():
        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)
    return venv_dir


def python_for_venv(venv_dir: Path) -> Path:
    if sys.platform.startswith('win'):
        return venv_dir / 'Scripts' / 'python.exe'
    return venv_dir / 'bin' / 'python'


def main() -> None:
    if not CAPABILITIES_DIR.exists():
        print(f'No capability directory found at {CAPABILITIES_DIR}')
        return

    for capability_dir in sorted(CAPABILITIES_DIR.iterdir()):
        if not capability_dir.is_dir():
            continue

        requirements_file = capability_dir / 'requirements.txt'
        venv_dir = ensure_venv(capability_dir)
        python_path = python_for_venv(venv_dir)

        if requirements_file.exists():
            subprocess.run(
                [str(python_path), '-m', 'pip', 'install', '-r', str(requirements_file)],
                check=True,
            )

        print(f'Prepared capability environment: {capability_dir.name}')


if __name__ == '__main__':
    main()
