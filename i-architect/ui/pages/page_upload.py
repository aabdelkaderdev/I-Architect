"""
Page 3: Upload & Extract — Document upload and extraction (FR-UI-012/013).

File upload, format validation, extraction strategy selection.
"""

import streamlit as st


def render() -> None:
    """Render the Upload & Extract page.

    Layout:
    - File uploader (PDF, DOCX, TXT, XLS/XLSX, CSV).
    - Extraction strategy selector (Line-by-Line, Regex, Grammar-Based, Hybrid).
    - Extract button → triggers extraction and shows progress.
    - Extraction result preview table.
    """
    st.header("📤 Upload & Extract")
    raise NotImplementedError
