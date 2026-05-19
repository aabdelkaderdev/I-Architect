import sys
from raa.utils.failure_register import FAILURE_REGISTER, get_failure_register


def test_failure_register_has_13_entries():
    """T027: FAILURE_REGISTER has exactly 13 entries covering Section 18 and Section 22H."""
    assert len(FAILURE_REGISTER) == 13


def test_failure_register_entries_have_required_fields():
    """T028: Every entry in FAILURE_REGISTER has all required non-empty string fields."""
    entries = get_failure_register()
    for entry in entries:
        assert isinstance(entry.risk_id, str) and entry.risk_id.strip()
        assert isinstance(entry.description, str) and entry.description.strip()
        assert isinstance(entry.mitigation_strategy, str) and entry.mitigation_strategy.strip()
        assert isinstance(entry.section_ref, str) and entry.section_ref.strip()
        assert isinstance(entry.verified_node, str) and entry.verified_node.strip()


def test_failure_register_risk_ids_unique():
    """T029: Every entry in FAILURE_REGISTER has a unique risk_id."""
    risk_ids = [entry.risk_id for entry in get_failure_register()]
    assert len(risk_ids) == len(set(risk_ids))


def _run_tests():
    """Run all tests defined in this module."""
    try:
        test_failure_register_has_13_entries()
        test_failure_register_entries_have_required_fields()
        test_failure_register_risk_ids_unique()
        print("All failure register tests passed successfully!")
        return True
    except AssertionError as exc:
        print(f"Assertion failed: {exc}", file=sys.stderr)
        return False
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return False


if __name__ == "__main__":
    ok = _run_tests()
    sys.exit(0 if ok else 1)
