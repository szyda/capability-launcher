from __future__ import annotations

from typing import Any, List, Literal, Optional

from pydantic import BaseModel, Field


InputType = Literal['text', 'textarea', 'number', 'checkbox', 'select']


class CapabilityField(BaseModel):
    name: str
    label: str
    type: InputType
    required: bool = False
    default: Optional[Any] = None
    options: Optional[List[str]] = None


class CapabilityMetadata(BaseModel):
    id: str
    name: str
    description: str
    version: str = '1.0.0'
    inputs: List[CapabilityField] = Field(default_factory=list)


class CapabilityRunRequest(BaseModel):
    inputs: dict[str, Any] = Field(default_factory=dict)


class CapabilityRunResponse(BaseModel):
    capability_id: str
    status: str
    result: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    duration_ms: int
