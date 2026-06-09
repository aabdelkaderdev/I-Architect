import os
import tempfile
import pytest
from ingestion.format_router import format_router_node, route_by_format
from ingestion.exceptions import EmptyFileError, UnsupportedFormatError

def test_empty_file():
    with tempfile.NamedTemporaryFile() as temp:
        # File is empty (0 bytes)
        state = {"file_path": temp.name}
        with pytest.raises(EmptyFileError):
            format_router_node(state)

def test_supported_extensions():
    # Test all supported extensions
    for ext, expected in [
        (".pdf", "pdf"),
        (".docx", "docx"),
        (".txt", "txt"),
        (".json", "json"),
        (".PDF", "pdf"),  # case insensitive
        (".Docx", "docx")
    ]:
        with tempfile.NamedTemporaryFile(suffix=ext) as temp:
            temp.write(b"content")
            temp.flush()
            state = {"file_path": temp.name}
            result = format_router_node(state)
            assert result == {"file_format": expected}

def test_unsupported_extension():
    with tempfile.NamedTemporaryFile(suffix=".xlsx") as temp:
        temp.write(b"content")
        temp.flush()
        state = {"file_path": temp.name}
        with pytest.raises(UnsupportedFormatError) as exc_info:
            format_router_node(state)
        assert ".xlsx" in str(exc_info.value)

def test_missing_file():
    state = {"file_path": "non_existent_file.pdf"}
    with pytest.raises(FileNotFoundError):
        format_router_node(state)

def test_route_by_format():
    state = {"file_format": "pdf"}
    assert route_by_format(state) == "pdf"
