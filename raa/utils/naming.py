"""Naming enforcement utilities — Phase 1 §7.5 naming convention validators.

Used by Pydantic validators on output models and optionally as pre-write checks in the registry.
Strict naming is enforced through LLM prompt design and output parsing, making identity checks
plain string equality with no fuzzy matching required.
"""

from raa.types import C4Type

_SUFFIX_MAP: dict[C4Type, str] = {
    "service": "Service",
    "database": "Database",
    "gateway": "Gateway",
    "queue": "Queue",
    "store": "Store",
    "external": "System",
    "actor": "",
}


def is_pascal_case(name: str) -> bool:
    """Returns whether `name` satisfies PascalCase rules.

    PascalCase: no spaces, hyphens, or underscores. Each word starts with a capital letter.
    Name may consist of a single word (e.g. "EndUser") or multiple concatenated words
    (e.g. "AuthenticationService").
    """
    if not name:
        return False
    # Reject spaces, hyphens, underscores
    if " " in name or "-" in name or "_" in name:
        return False
    # Must start with an uppercase letter
    if not name[0].isupper():
        return False
    # All characters must be alphanumeric
    return name.isalnum()


def expected_suffix(c4_type: C4Type) -> str:
    """Returns the mandatory suffix for `c4_type`, or empty string for actors.

    Mapping (Phase 1 §7.5):
        "service"  → "Service"
        "database" → "Database"
        "gateway"  → "Gateway"
        "queue"    → "Queue"
        "store"    → "Store"
        "external" → "System"
        "actor"    → "" (no suffix)
    """
    return _SUFFIX_MAP[c4_type]


def has_correct_suffix(name: str, c4_type: C4Type) -> bool:
    """Returns whether `name` satisfies suffix rules.

    For c4_type values other than "actor", the name must end with the mandatory suffix.
    For "actor", PascalCase alone is sufficient — no suffix is required.
    """
    suffix = expected_suffix(c4_type)
    if not suffix:
        return True
    return name.endswith(suffix) and name != suffix


def normalize_name(name: str, c4_type: C4Type) -> str:
    """Pre: `name` is PascalCase or can be deterministically suffix-normalized.

    Post: Returns normalized canonical name.

    If a name passes the type check but fails the suffix rule (e.g., the LLM outputs
    "Authentication" instead of "AuthenticationService"), this function attempts a
    deterministic suffix append before raising a validation error. This is a pragmatic
    concession to LLM imperfection: pure rejection requires a retry loop; deterministic
    correction is cheaper and fully auditable in the batch output.
    """
    if has_correct_suffix(name, c4_type):
        return name

    suffix = expected_suffix(c4_type)
    if not suffix:
        return name

    known_suffixes = {"Service", "Database", "Gateway", "Queue", "Store", "System"}
    for bad_suffix in known_suffixes:
        if bad_suffix == suffix:
            continue
        if name.endswith(bad_suffix) and len(name) > len(bad_suffix):
            stripped = name[:-len(bad_suffix)]
            if stripped and stripped[0].isupper():
                if has_correct_suffix(stripped, c4_type):
                    return stripped
                corrected = stripped + suffix
                if is_pascal_case(corrected):
                    return corrected

    corrected = name + suffix
    # Only accept the correction if the result is still valid PascalCase
    if is_pascal_case(corrected):
        return corrected

    raise ValueError(
        f"Cannot normalize name {name!r} for c4_type {c4_type!r}"
    )
