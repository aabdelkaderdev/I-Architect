"""
JsonPlusSerializer-compatible serialization helpers.

All RAA dataclasses use @dataclass (stdlib) and JSON-primitive field types,
so they are natively supported by LangGraph's default JsonPlusSerializer.
These helpers provide explicit to/from JSON routines for testing, debugging,
and the final C4-compliant JSON handoff to AGA.

Usage:
    from raa.state.serialization import to_json, from_json
    from raa.state.types import ArchModel

    json_str = to_json(model)
    restored = from_json(json_str, ArchModel)
"""
from __future__ import annotations

import dataclasses
import json
from typing import get_args, get_origin, get_type_hints

# Types that are always safe for JSON serialization
_PRIMITIVES = (str, int, float, bool, type(None))


def validate_serializable_fields(obj, path: str = "$") -> None:
    """Verify all fields contain only JSON-serializable types.

    Raises TypeError with the field path if a non-serializable type
    (Callable, ModuleType, raw object, etc.) is found. Call before
    serialization to ensure checkpoint compatibility.

    Args:
        obj: A dataclass instance or nested value to validate.
        path: Current field path for error messages.

    Raises:
        TypeError: If a non-serializable type is found.
    """
    if dataclasses.is_dataclass(obj):
        for field in dataclasses.fields(obj):
            validate_serializable_fields(getattr(obj, field.name), f"{path}.{field.name}")
    elif isinstance(obj, (list, tuple)):
        for i, item in enumerate(obj):
            validate_serializable_fields(item, f"{path}[{i}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            validate_serializable_fields(v, f"{path}.{k}")
    elif isinstance(obj, _PRIMITIVES):
        pass
    else:
        raise TypeError(
            f"Non-serializable type {type(obj).__name__!r} at {path}. "
            f"Only str, int, float, bool, None, list, dict, "
            f"and @dataclass types are supported by JsonPlusSerializer."
        )


def dataclass_to_dict(obj) -> dict | list | str | int | float | bool | None:
    """Recursively convert a dataclass to plain dicts/lists.

    Args:
        obj: A @dataclass instance or primitive value.

    Returns:
        Plain Python dict/list/primitive suitable for json.dumps.
    """
    if dataclasses.is_dataclass(obj):
        return {
            field.name: dataclass_to_dict(getattr(obj, field.name))
            for field in dataclasses.fields(obj)
        }
    if isinstance(obj, (list, tuple)):
        return [dataclass_to_dict(item) for item in obj]
    if isinstance(obj, dict):
        # Convert non-string keys to strings for JSON compatibility
        return {str(k): dataclass_to_dict(v) for k, v in obj.items()}
    return obj


def _resolve_type(type_hint):
    """Resolve a type annotation to its (origin, args) pair."""
    origin = get_origin(type_hint)
    args = get_args(type_hint)
    if origin is not None:
        return origin, args
    return type_hint, ()


def dict_to_dataclass(data, target_type: type):
    """Recursively reconstruct a dataclass from a plain dict.

    Handles nested dataclasses, list[Dataclass], and dict fields.
    Uses type annotations from the target dataclass to determine
    how to reconstruct each field.

    Args:
        data: A dict (or primitive) to convert.
        target_type: The target @dataclass type.

    Returns:
        An instance of target_type populated from data.
    """
    if data is None:
        return None

    if not dataclasses.is_dataclass(target_type):
        return data

    hints = get_type_hints(target_type)

    kwargs: dict[str, object] = {}
    for field in dataclasses.fields(target_type):
        field_name = field.name
        if field_name not in data:
            continue

        value = data[field_name]
        field_type = hints.get(field_name)
        if field_type is None:
            kwargs[field_name] = value
            continue

        origin, args = _resolve_type(field_type)

        # Handle nested dataclass
        if dataclasses.is_dataclass(field_type):
            kwargs[field_name] = dict_to_dataclass(value, field_type)
        # Handle list[Dataclass]
        elif origin is list and args and dataclasses.is_dataclass(args[0]):
            kwargs[field_name] = [
                dict_to_dataclass(item, args[0]) for item in (value or [])
            ]
        # Handle Optional[Dataclass] = Union[Dataclass, None]
        elif origin is not None and hasattr(origin, "__args__"):
            # Check for Union/Optional with a dataclass
            union_args = get_args(field_type)
            dc_arg = next(
                (a for a in union_args if dataclasses.is_dataclass(a)), None
            )
            if dc_arg is not None and value is not None:
                kwargs[field_name] = dict_to_dataclass(value, dc_arg)
            else:
                kwargs[field_name] = value
        else:
            kwargs[field_name] = value

    return target_type(**kwargs)


def to_json(obj) -> str:
    """Serialize a dataclass to a JSON string.

    Args:
        obj: A @dataclass instance.

    Returns:
        JSON string representation.

    Raises:
        TypeError: If obj contains non-serializable field types.
    """
    validate_serializable_fields(obj)
    return json.dumps(dataclass_to_dict(obj), indent=2, default=str)


def from_json(json_str: str, target_type: type):
    """Deserialize a JSON string back to a dataclass.

    Args:
        json_str: JSON string produced by to_json().
        target_type: The @dataclass type to reconstruct.

    Returns:
        An instance of target_type.
    """
    data = json.loads(json_str)
    return dict_to_dataclass(data, target_type)
