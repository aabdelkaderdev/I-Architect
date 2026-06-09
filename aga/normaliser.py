"""RAA normalisation — parse the raw RAA output dict into typed RAAOutput.

Pure function with no I/O, no side effects, no LLM calls.
"""

from __future__ import annotations

from pydantic import ValidationError

from aga.schemas import (
    RAAL1Description,
    RAAL2Description,
    RAAL3Description,
    RAAEntityRegistryEntry,
    RAAOutput,
)


class NormalisationError(ValueError):
    """Raised when the RAA output dict cannot be parsed into RAAOutput."""


_REQUIRED_KEYS = frozenset(
    {"l1_description", "l2_descriptions", "l3_descriptions", "entity_registry"}
)


def normalise_raa_output(raw: dict) -> RAAOutput:
    """Parse and validate the raw RAA output dict into a typed RAAOutput.

    Parameters
    ----------
    raw : dict
        The plain dict exactly as returned by the RAA graph.

    Returns
    -------
    RAAOutput
        Fully typed representation of the RAA output.

    Raises
    ------
    NormalisationError
        If a required top-level key is missing or a sub-structure cannot
        be parsed into its expected type.
    """
    if not isinstance(raw, dict):
        raise NormalisationError(
            f"Expected a dict, got {type(raw).__name__}"
        )

    missing = _REQUIRED_KEYS - raw.keys()
    if missing:
        raise NormalisationError(
            f"Missing required top-level keys: {sorted(missing)}"
        )

    try:
        l1 = RAAL1Description.model_validate(raw["l1_description"])
    except ValidationError as exc:
        raise NormalisationError(_fmt_path("l1_description", exc)) from exc

    l2_descriptions = _parse_list(
        raw["l2_descriptions"], RAAL2Description, "l2_descriptions"
    )

    l3_descriptions = _parse_list(
        raw["l3_descriptions"], RAAL3Description, "l3_descriptions"
    )

    entity_registry = _parse_entity_registry(raw["entity_registry"])

    return RAAOutput(
        l1_description=l1,
        l2_descriptions=l2_descriptions,
        l3_descriptions=l3_descriptions,
        entity_registry=entity_registry,
        coverage_gaps=raw.get("coverage_gaps", []),
        conflicts=raw.get("conflicts", []),
    )


def _parse_list(
    raw_list: object, model: type, parent_path: str
) -> list:
    if not isinstance(raw_list, list):
        raise NormalisationError(
            f"Expected a list at '{parent_path}', got {type(raw_list).__name__}"
        )
    result = []
    for i, item in enumerate(raw_list):
        item_path = f"{parent_path}[{i}]"
        try:
            result.append(model.model_validate(item))
        except ValidationError as exc:
            raise NormalisationError(_fmt_path(item_path, exc)) from exc
    return result


def _parse_entity_registry(raw_registry: object) -> dict[str, RAAEntityRegistryEntry]:
    if not isinstance(raw_registry, dict):
        raise NormalisationError(
            f"Expected a dict at 'entity_registry', got {type(raw_registry).__name__}"
        )
    result = {}
    for key, value in raw_registry.items():
        key_path = f"entity_registry.{key}"
        try:
            result[key] = RAAEntityRegistryEntry.model_validate(value)
        except ValidationError as exc:
            raise NormalisationError(_fmt_path(key_path, exc)) from exc
    return result


def _fmt_path(path: str, exc: ValidationError) -> str:
    locs = []
    for err in exc.errors():
        loc = " -> ".join(str(p) for p in err["loc"])
        locs.append(f"{path}.{loc}" if loc else path)
    joined = "; ".join(locs)
    return f"{joined}: {exc.error_count()} validation error(s)"
