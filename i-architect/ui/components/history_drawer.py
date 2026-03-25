"""
History Drawer Component — Slide-out panel for output history (FR-UI-003–005).

Shows file explorer tree with generated outputs per agent,
allows version selection, deletion via swipe, and timestamp display.
"""

import streamlit as st


def render_history_drawer() -> None:
    """Render the history drawer as a sidebar overlay.

    Features:
    - File tree grouped by agent (raa_output/, aga_output/, sa_output/).
    - Each file shows timestamp and size.
    - Selection sets 'active version' for MCP Aggregator reference.
    - Swipe-to-delete with confirmation (FR-UI-005).
    """
    raise NotImplementedError


def _toggle_drawer() -> None:
    """Toggle the history drawer visibility."""
    st.session_state["history_drawer_open"] = not st.session_state.get("history_drawer_open", False)
