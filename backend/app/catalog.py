"""Responsible for loading and exposing capability metadata discovered from capability folders."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from .models import CapabilityMetadata

logger = logging.getLogger(__name__)


class CapabilityCatalog:
    """Loads capability metadata from the capabilities directory."""

    def __init__(self, capabilities_dir: str | Path):
        self.capabilities_dir = Path(capabilities_dir)
        self.capabilities: dict[str, CapabilityMetadata] = {}
        self.load()

    def load(self) -> None:
        if not self.capabilities_dir.exists():
            logger.info('Capability directory does not exist: %s', self.capabilities_dir)
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
                logger.warning('Skipping invalid capability manifest %s: %s', manifest_path, exc)
                continue

            existing = self.capabilities.get(metadata.id)
            if existing is not None:
                logger.warning('Duplicate capability id %s detected; overriding previous definition.', metadata.id)

            self.capabilities[metadata.id] = metadata

    def get(self, capability_id: str) -> Optional[CapabilityMetadata]:
        return self.capabilities.get(capability_id)

    def list(self) -> list[CapabilityMetadata]:
        return list(self.capabilities.values())
