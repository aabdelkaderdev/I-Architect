"""
Page 8: SA — Scoring Agent results (FR-UI-021/022).

4-pillar radar chart, drawbacks list, adjustments, regeneration recommendation.
"""

import streamlit as st


def render() -> None:
    """Render the SA evaluation results page.

    Layout:
    - Overall score badge (total_percent_correct).
    - Radar chart: 4 pillars (Syntax, Traceability, Fidelity, SAAM).
    - Drawbacks table: Severity, Category, Description, Affected Entities.
    - Adjustments needed list.
    - Regeneration recommendation banner (if total < 70% or any pillar < 50%).
    - Download evaluation JSON button (FR-UI-022).
    - Download PDF report button (FR-UI-021).
    """
    st.header("📊 SA — Architectural Evaluation")
    raise NotImplementedError
