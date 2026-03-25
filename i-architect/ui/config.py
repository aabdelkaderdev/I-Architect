"""
UI Configuration — Constants and settings for the Streamlit frontend.
"""

import os

# Backend API URL
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

# SSE polling interval (seconds)
SSE_POLL_INTERVAL = 2

# Page definitions (name, icon, label, requires_project)
PAGES = [
    {"key": "projects", "icon": "📁", "label": "Projects", "requires_project": False},
    {"key": "workflow", "icon": "⚙️", "label": "Workflow", "requires_project": True},
    {"key": "upload", "icon": "📤", "label": "Upload", "requires_project": True},
    {"key": "requirements", "icon": "📝", "label": "Requirements", "requires_project": True},
    {"key": "arlo", "icon": "🎯", "label": "ARLO", "requires_project": True},
    {"key": "raa", "icon": "🔍", "label": "RAA", "requires_project": True},
    {"key": "aga", "icon": "🏗️", "label": "AGA", "requires_project": True},
    {"key": "sa", "icon": "📊", "label": "SA", "requires_project": True},
]
