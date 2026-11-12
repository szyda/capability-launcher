"""Responsible for preparing the capability runtime and executing a capability in isolation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from .config import CAPABILITIES_DIR, DEFAULT_TIMEOUT_SECONDS, WORKER_PATH


class CapabilityExecutionError(RuntimeError):
    """Raised when a capability fails at runtime."""


class CapabilityTimeoutError(CapabilityExecutionError):
    """Raised when a capability exceeds the allowed execution time."""


class CapabilityNotReadyError(CapabilityExecutionError):
    """Raised when the capability virtual environment is not available."""


def get_capability_python(capability_id: str) -> Path:
    capability_dir = CAPABILITIES_DIR / capability_id
    venv_bin = 'Scripts' if sys.platform.startswith('win') else 'bin'
    python_name = 'python.exe' if sys.platform.startswith('win') else 'python'
    return capability_dir / '.venv' / venv_bin / python_name


def execute_capability(capability_id: str, inputs: dict) -> dict:
    capability_dir = CAPABILITIES_DIR / capability_id
    python_path = get_capability_python(capability_id)

    if not python_path.exists():
        raise CapabilityNotReadyError(f'Capability environment is not ready for {capability_id}')

    try:
        completed = subprocess.run(
            [str(python_path), str(WORKER_PATH), str(capability_dir), json.dumps(inputs)],
            capture_output=True,
            text=True,
            timeout=DEFAULT_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise CapabilityTimeoutError('Execution timed out') from exc

    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or 'Capability execution failed'
        raise CapabilityExecutionError(message)

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise CapabilityExecutionError('Capability returned invalid JSON') from exc

    if payload.get('ok') is not True:
        raise CapabilityExecutionError(payload.get('error', 'Capability execution failed'))

    return payload.get('result', {})
