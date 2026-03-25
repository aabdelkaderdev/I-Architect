"""
Page 5: ARLO — Optimization configuration and results (FR-UI-016/017).

Strategy selector, batch size, read-only decision view with user notes.
"""

import streamlit as st


def render() -> None:
    """Render the ARLO page.

    Layout:
    - Optimization strategy toggle (ILP / Greedy) (FR-UI-016).
    - Batch size slider.
    - Decision results table (read-only): Category, Pattern, Score, QAs.
    - User notes textarea per decision (appended, never overwrite) (FR-UI-017).
    - Sensitivity analysis results (if Workflow 3).
    """
    st.header("🎯 ARLO — Architecture Optimization")
    raise NotImplementedError
