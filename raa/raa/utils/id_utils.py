"""
RAA-internal requirement ID normalization.

Requirement IDs are stored in "R{id}" format (e.g. "R5"). This module
provides the single canonical conversion from raw ARLO IDs.
"""

from __future__ import annotations

import re


_NUMERIC_R_ID = re.compile(r"^r(\d+)$", re.IGNORECASE)
_NUMERIC_RN_ID = re.compile(r"^rn(\d+)$", re.IGNORECASE)


def to_r_id(raw_id) -> str:
    """Convert a raw requirement ID to canonical RAA "R{id}" format.

    Handles: integers, strings with/without R prefix, whitespace,
    lowercase prefixes, and integer-only strings.

    Returns an "R{id}" string where {id} is the numeric identifier.
    """
    s = str(raw_id).strip()
    if not s:
        return s

    numeric_match = _NUMERIC_R_ID.match(s)
    if numeric_match:
        return f"R{numeric_match.group(1)}"

    rn_match = _NUMERIC_RN_ID.match(s)
    if rn_match:
        return f"RN{rn_match.group(1)}"

    return f"R{s}"
