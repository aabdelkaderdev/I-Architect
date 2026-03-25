"""
LLM Config Modal Component — LLM instance management (FR-UI-026).

CRUD interface for managing LLM configurations stored in session state.
"""

import streamlit as st


def render_llm_config_modal() -> None:
    """Render the LLM configuration management modal.

    Features:
    - Add new LLM (name, provider, model, endpoint, API key, temperature).
    - Edit existing LLM configs.
    - Delete LLM configs.
    - Health check button per LLM.
    - All configs stored in st.session_state["llm_configs"].
    """
    raise NotImplementedError
