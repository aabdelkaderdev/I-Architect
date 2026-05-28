import pytest
import os
from unittest.mock import Mock, MagicMock
from langchain_core.language_models import BaseChatModel

from ingestion.schema import IngestionState, IngestionContext, IngestionConfig, FilterConfig
from ingestion.graph import (
    build_ingestion_graph,
    output_assembly_node,
    rfa_node
)
from ingestion.exceptions import EmptyRequirementsError
from ingestion.format_router import route_by_format

def test_conditional_routing():
    """6.1 Verify conditional routing for each format."""
    assert route_by_format({"file_format": "pdf"}) == "pdf"
    assert route_by_format({"file_format": "docx"}) == "docx"
    assert route_by_format({"file_format": "txt"}) == "txt"
    assert route_by_format({"file_format": "json"}) == "json"
    
    with pytest.raises(ValueError):
        route_by_format({"file_format": "unknown"})

def test_output_assembly_empty_requirements_error():
    """6.2 Verify EmptyRequirementsError in the output assembly node."""
    state = {
        "extracted_requirements": {}
    }
    with pytest.raises(EmptyRequirementsError):
        output_assembly_node(state)
        
    state = {
        "extracted_requirements": {"REQ-1": "Valid text"}
    }
    result = output_assembly_node(state)
    assert result == {"extracted_requirements": {"REQ-1": "Valid text"}}

def test_checkpointing_resume_behaviour(tmp_path):
    """6.3 Verify checkpointer compilation with db_path."""
    db_path = str(tmp_path / "checkpoints.db")
    graph = build_ingestion_graph(db_path=db_path)
    
    assert graph.checkpointer is not None
    assert os.path.exists(db_path)
    
    # Test fallback if db_path is invalid/directory
    invalid_db_path = str(tmp_path)
    graph_fallback = build_ingestion_graph(db_path=invalid_db_path)
    assert graph_fallback.checkpointer is None

def test_rfa_context_injection(monkeypatch):
    """6.4 Verify context injection (Runtime[IngestionContext]) is accessible in the RFA node."""
    # We will mock filter_requirements to avoid running actual LLM code
    mock_filter = Mock(return_value=({"REQ-1": "Clean"}, None))
    monkeypatch.setattr("ingestion.graph.filter_requirements", mock_filter)
    
    mock_llm = MagicMock(spec=BaseChatModel)
    
    state = {
        "file_path": "test.txt",
        "file_format": "txt",
        "extracted_requirements": {"REQ-1": "Raw"},
        "ingestion_config": IngestionConfig(),
        "filter_config": FilterConfig(enabled=True, skip_filter_for_json=False)
    }
    
    # Create a mock Runtime
    mock_runtime = MagicMock()
    mock_runtime.context = IngestionContext(llm=mock_llm)
    
    result = rfa_node(state, mock_runtime)
    
    assert result == {"extracted_requirements": {"REQ-1": "Clean"}, "filter_report": None}
    mock_filter.assert_called_once()
    # verify llm from context was passed
    assert mock_filter.call_args[0][1] is mock_llm
