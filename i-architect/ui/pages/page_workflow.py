"""
Page 2: Workflow Selection — Pipeline configuration (FR-UI-009/010/011).

Workflow type selection, ARLO toggle, LLM ↔ Agent mapping, pre-flight checks.
"""

import streamlit as st


def render() -> None:
    """Render the Workflow configuration page.

    Layout:
    - Workflow type selector (1, 2, 3) with visual descriptions.
    - ARLO Enable/Disable toggle (FR-UI-009).
    - LLM ↔ Agent mapping matrix (dropdown per agent × LLM) (FR-UI-010).
    - Pre-flight check button: validates LLM health before Run (FR-UI-011).
    - Run Pipeline button.
    """
    st.header("⚙️ Workflow Configuration")
    raise NotImplementedError
