"""Responsible for loading and exposing capability metadata discovered from capability folders."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from .models import CapabilityMetadata


class CapabilityCatalog:
    """Loads capability metadata from the capabilities directory."""

    def __init__(self, capabilities_dir: str | Path):
        self.capabilities_dir = Path(capabilities_dir)
        self.capabilities: dict[str, CapabilityMetadata] = {}
        self.load()

    def load(self) -> None:
        if not self.capabilities_dir.exists():
            return

        for child in sorted(self.capabilities_dir.iterdir()):
            if not child.is_dir():
                continue

            manifest_path = child / 'manifest.json'
            if not manifest_path.exists():
                continue

            try:
                payload = json.loads(manifest_path.read_text())
                metadata = CapabilityMetadata.model_validate(payload)
            except (json.JSONDecodeError, TypeError, ValueError, OSError) as exc:
                logging.warning('Skipping capability manifest %s: %s', manifest_path, exc)
                continue

            self.capabilities[metadata.id] = metadata

    def get(self, capability_id: str) -> Optional[CapabilityMetadata]:
        return self.capabilities.get(capability_id)

    def list(self) -> list[CapabilityMetadata]:
        return list(self.capabilities.values())
