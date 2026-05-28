import os
from ingestion.schema import IngestionState
from ingestion.exceptions import EmptyFileError, UnsupportedFormatError

_FORMAT_MAP: dict[str, str] = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".txt": "txt",
    ".json": "json",
}

def format_router_node(state: IngestionState) -> dict:
    file_path = state["file_path"]
    
    # Let FileNotFoundError propagate natively
    if os.path.getsize(file_path) == 0:
        raise EmptyFileError("Input file is 0 bytes.")
        
    _, ext = os.path.splitext(file_path.lower())
    
    if ext not in _FORMAT_MAP:
        raise UnsupportedFormatError(f"Unsupported format: {ext}")
        
    canonical_format = _FORMAT_MAP[ext]
    
    return {"file_format": canonical_format}

def route_by_format(state: IngestionState) -> str:
    """Routing function for add_conditional_edges."""
    return state["file_format"]
