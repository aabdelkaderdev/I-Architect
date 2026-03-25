"""
Topbar Component — Persistent navigation bar (FR-UI-002).

Always visible, contains: project name, pipeline step indicators,
LLM Config button, History Drawer toggle.
"""

import streamlit as st
from config import PAGES


def render_topbar() -> None:
    """Render the persistent topbar with navigation and status indicators.

    Layout:
    [Project Name] | [Step Indicators 1-8] | [LLM Config ⚙️] | [History 📜]
    """
    raise NotImplementedError


def _navigate_to(page_key: str) -> None:
    """Update session state to navigate to a page.

    Args:
        page_key: Page identifier from PAGES config.
    """
    st.session_state["current_page"] = page_key
