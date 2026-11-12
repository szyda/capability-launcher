from __future__ import annotations

from typing import Any


def validate_inputs(definitions: list[dict[str, Any]], inputs: dict[str, Any]) -> None:
    errors: dict[str, str] = {}

    for field in definitions:
        name = field['name']
        if field.get('required') and name not in inputs:
            errors[name] = 'This field is required.'
            continue

        if name not in inputs:
            continue

        value = inputs[name]
        field_type = field['type']

        if field_type in {'text', 'textarea'}:
            ok = isinstance(value, str)
        elif field_type == 'number':
            ok = isinstance(value, (int, float)) and not isinstance(value, bool)
        elif field_type == 'checkbox':
            ok = isinstance(value, bool)
        elif field_type == 'select':
            options = field.get('options') or []
            ok = value in options if options else isinstance(value, str)
        else:
            ok = True

        if not ok:
            errors[name] = 'Invalid input type.'

    if errors:
        raise ValueError(errors)
