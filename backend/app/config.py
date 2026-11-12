"""Application-wide configuration and path constants for the capability platform."""

from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
CAPABILITIES_DIR = BACKEND_DIR / 'capabilities'
WORKER_PATH = BACKEND_DIR / 'runner' / 'worker.py'
DEFAULT_TIMEOUT_SECONDS = 10
