import pytest
from unittest.mock import MagicMock
from ingestion.rfa import filter_requirements
from ingestion.schema import FilterBatch, FilteredRequirement
from ingestion.graph import rfa_node
from ingestion.schema import IngestionState, IngestionConfig, FilterConfig, IngestionContext

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    chain = MagicMock()
    # Chain returns whatever we configure it to return
    llm.with_structured_output.return_value = chain
    chain.with_retry.return_value = chain
    return llm, chain

def test_filter_requirements_batching(mock_llm):
    llm, chain = mock_llm
    
    # 5 requirements, batch size 2 -> should result in 3 batches
    reqs = {f"REQ-{i}": f"Text {i}" for i in range(5)}
    
    # Mock chain to return all SIGNALs
    def mock_invoke(*args, **kwargs):
        # We need to extract the IDs from the JSON batch sent to invoke
        import json
        messages = args[0]
        batch_json = messages[1].content
        items = json.loads(batch_json)
        
        batch = FilterBatch(requirements=[
            FilteredRequirement(id=item["id"], classification="SIGNAL", confidence=0.9, reason="test")
            for item in items
        ])
        return batch
        
    chain.invoke.side_effect = mock_invoke
    
    res, report = filter_requirements(reqs, llm, confidence_threshold=0.7, batch_size=2, log_dropped=False, emit_report=True)
    
    assert chain.invoke.call_count == 3
    assert len(res) == 5
    assert report["total_input"] == 5
    assert report["total_signal"] == 5

def test_filter_requirements_threshold_logic(mock_llm):
    llm, chain = mock_llm
    
    reqs = {
        "REQ-1": "Signal requirement",
        "REQ-2": "Confident noise",
        "REQ-3": "Uncertain noise"
    }
    
    chain.invoke.return_value = FilterBatch(requirements=[
        FilteredRequirement(id="REQ-1", classification="SIGNAL", confidence=0.5, reason="signal"),
        FilteredRequirement(id="REQ-2", classification="NOISE", confidence=0.8, reason="noise 1"),
        FilteredRequirement(id="REQ-3", classification="NOISE", confidence=0.4, reason="noise 2"),
    ])
    
    res, report = filter_requirements(reqs, llm, confidence_threshold=0.7, batch_size=10, log_dropped=False, emit_report=True)
    
    # Signal is kept (even with low confidence)
    # Uncertain noise (<0.7) is kept
    # Confident noise (>=0.7) is dropped
    assert set(res.keys()) == {"REQ-1", "REQ-3"}
    assert report["total_input"] == 3
    assert report["total_signal"] == 1
    assert report["total_noise_dropped"] == 1
    assert report["total_noise_kept"] == 1
    
    assert len(report["dropped_requirements"]) == 1
    assert report["dropped_requirements"][0]["id"] == "REQ-2"
    
    assert len(report["noise_kept_below_threshold"]) == 1
    assert report["noise_kept_below_threshold"][0]["id"] == "REQ-3"

def test_rfa_node_bypass_disabled():
    state = IngestionState(
        file_path="/test.pdf",
        extracted_requirements={"R-1": "test"},
        ingestion_config=IngestionConfig(),
        filter_config=FilterConfig(enabled=False)
    )
    context = IngestionContext(llm=MagicMock())
    runtime = MagicMock()
    runtime.context = context
    
    out = rfa_node(state, runtime)
    
    assert out["extracted_requirements"] == {"R-1": "test"}
    assert out["filter_report"] is None
    context.llm.with_structured_output.assert_not_called()

def test_rfa_node_bypass_json_skip():
    state = IngestionState(
        file_path="/test.json",
        extracted_requirements={"R-1": "test"},
        ingestion_config=IngestionConfig(),
        filter_config=FilterConfig(enabled=True, skip_filter_for_json=True)
    )
    context = IngestionContext(llm=MagicMock())
    runtime = MagicMock()
    runtime.context = context
    
    out = rfa_node(state, runtime)
    
    assert out["extracted_requirements"] == {"R-1": "test"}
    assert out["filter_report"] is None
    context.llm.with_structured_output.assert_not_called()
