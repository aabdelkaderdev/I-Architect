"""
I-Architect v2.3 — Streamlit SPA Entry Point.

Implements: FR-UI-001 (session-state-based routing, persistent topbar).
"""

import streamlit as st


def main() -> None:
    """Main application entry point.

    Configures page layout, initializes session state, and renders
    the current page based on st.session_state["current_page"].
    """
    st.set_page_config(
        page_title="I-Architect v2.3",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # ── Initialize session state ──
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "projects"
    if "selected_project_id" not in st.session_state:
        st.session_state["selected_project_id"] = None
    if "llm_configs" not in st.session_state:
        st.session_state["llm_configs"] = []
    if "history_drawer_open" not in st.session_state:
        st.session_state["history_drawer_open"] = False

    # ── Render persistent topbar ──
    from components.topbar import render_topbar
    render_topbar()

    # ── Page router ──
    _route_page()


def _route_page() -> None:
    """Route to the current page based on session state (FR-UI-001)."""
    page = st.session_state.get("current_page", "projects")

    page_map = {
        "projects": "pages.page_projects",
        "workflow": "pages.page_workflow",
        "upload": "pages.page_upload",
        "requirements": "pages.page_requirements",
        "arlo": "pages.page_arlo",
        "raa": "pages.page_raa",
        "aga": "pages.page_aga",
        "sa": "pages.page_sa",
    }

    if page in page_map:
        import importlib
        module = importlib.import_module(page_map[page])
        module.render()
    else:
        st.error(f"Unknown page: {page}")


if __name__ == "__main__":
    main()
