"""Tests for naming validators. Per FG-Phase-44 §2."""

from __future__ import annotations

import pytest

from raa.utils.naming import (
    expected_suffix,
    has_correct_suffix,
    is_pascal_case,
    normalize_name,
)


class TestNaming:
    def test_is_pascal_case_valid(self):
        """Valid PascalCase names pass."""
        assert is_pascal_case("AuthenticationService") is True
        assert is_pascal_case("EndUser") is True
        assert is_pascal_case("ApiGateway") is True
        assert is_pascal_case("Service") is True

    def test_is_pascal_case_invalid(self):
        """Invalid names are rejected."""
        assert is_pascal_case("") is False
        assert is_pascal_case("auth-service") is False
        assert is_pascal_case("not PascalCase") is False
        assert is_pascal_case("lowercase") is False
        assert is_pascal_case("snake_case_name") is False

    def test_expected_suffix_per_type(self):
        """Each c4_type maps to its mandatory suffix."""
        assert expected_suffix("service") == "Service"
        assert expected_suffix("database") == "Database"
        assert expected_suffix("gateway") == "Gateway"
        assert expected_suffix("queue") == "Queue"
        assert expected_suffix("store") == "Store"
        assert expected_suffix("external") == "System"
        assert expected_suffix("actor") == ""

    def test_has_correct_suffix(self):
        """Suffix validation matches Phase 1 §7.5 rules."""
        assert has_correct_suffix("AuthenticationService", "service") is True
        assert has_correct_suffix("UserDatabase", "database") is True
        assert has_correct_suffix("EndUser", "actor") is True
        assert has_correct_suffix("Auth", "service") is False
        assert has_correct_suffix("Service", "service") is False  # name IS the suffix

    def test_normalize_name_appends_suffix(self):
        """Names missing suffix get it appended deterministically."""
        assert normalize_name("Authentication", "service") == "AuthenticationService"
        assert normalize_name("AuthService", "service") == "AuthService"  # already correct
        assert normalize_name("EndUser", "actor") == "EndUser"  # no suffix for actor
        assert normalize_name("OfficerSessionStore", "database") == "OfficerSessionDatabase"
        assert normalize_name("SecureGatewayService", "gateway") == "SecureGateway"

        # Invalid correction raises
        with pytest.raises(ValueError):
            normalize_name("not-valid", "service")
