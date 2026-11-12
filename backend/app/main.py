"""FastAPI entry point for the capability platform."""

from __future__ import annotations

import logging
from time import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .catalog import CapabilityCatalog
from .config import CAPABILITIES_DIR
from .executor import CapabilityExecutionError, CapabilityNotReadyError, CapabilityTimeoutError, execute_capability
from .models import CapabilityRunRequest, CapabilityRunResponse
from .validation import validate_inputs

logger = logging.getLogger(__name__)

app = FastAPI(title='Capability Launcher', version='0.1.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
catalog = CapabilityCatalog(CAPABILITIES_DIR)
logger.info('Loaded %d capabilities from %s', len(catalog.list()), CAPABILITIES_DIR)


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}


@app.get('/api/capabilities')
def list_capabilities() -> dict[str, list[dict[str, object]]]:
    return {'capabilities': [capability.model_dump(mode='json') for capability in catalog.list()]}


@app.get('/api/capabilities/{capability_id}')
def get_capability(capability_id: str) -> dict[str, object]:
    capability = catalog.get(capability_id)
    if capability is None:
        logger.warning('Capability lookup failed for unknown id: %s', capability_id)
        raise HTTPException(status_code=404, detail={'error': 'Capability not found', 'capability_id': capability_id})
    return capability.model_dump(mode='json')


@app.post('/api/capabilities/{capability_id}/run', response_model=CapabilityRunResponse)
def run_capability(capability_id: str, request: CapabilityRunRequest) -> CapabilityRunResponse:
    capability = catalog.get(capability_id)
    if capability is None:
        logger.warning('Execution request rejected for unknown capability: %s', capability_id)
        raise HTTPException(status_code=404, detail={'error': 'Capability not found', 'capability_id': capability_id})

    try:
        validate_inputs([field.model_dump(mode='json') for field in capability.inputs], request.inputs)
    except ValueError as exc:
        logger.warning('Invalid input payload for %s: %s', capability_id, exc)
        raise HTTPException(status_code=422, detail={'error': 'Invalid inputs', 'details': str(exc)}) from exc

    try:
        started = time()
        result = execute_capability(capability_id, request.inputs)
    except CapabilityTimeoutError as exc:
        logger.warning('Execution timed out for capability %s', capability_id)
        raise HTTPException(status_code=504, detail={'error': 'Execution timed out'}) from exc
    except CapabilityNotReadyError as exc:
        logger.error('Capability environment not ready for %s', capability_id)
        raise HTTPException(status_code=500, detail={'error': 'Capability environment is not ready'}) from exc
    except CapabilityExecutionError as exc:
        logger.error('Capability execution failed for %s: %s', capability_id, exc)
        raise HTTPException(status_code=500, detail={'error': str(exc)}) from exc

    duration_ms = int((time() - started) * 1000)
    return CapabilityRunResponse(
        capability_id=capability_id,
        status='success',
        result=result,
        duration_ms=duration_ms,
    )
