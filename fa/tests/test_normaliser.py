import pytest
from ingestion.normaliser import normalise_blocks
from ingestion.schema import IngestionConfig
from ingestion.exceptions import EmptyRequirementsError

def test_normalise_blocks_sequential_ids():
    cfg = IngestionConfig(id_prefix="TEST-", min_block_length=10, max_block_length=100, dedup_enabled=False)
    blocks = [{"text": "First requirement string."}]
    
    reqs = normalise_blocks(blocks, cfg)
    assert reqs == {"TEST-1": "First requirement string."}

def test_normalise_blocks_inline_ids():
    cfg = IngestionConfig(min_block_length=10, max_block_length=100, dedup_enabled=False)
    blocks = [
        {"text": "First requirement string.", "inline_id": "IN-1"},
        {"text": "Second requirement string.", "inline_id": "IN-2"}
    ]
    
    reqs = normalise_blocks(blocks, cfg)
    assert reqs == {"IN-1": "First requirement string.", "IN-2": "Second requirement string."}

def test_normalise_blocks_duplicate_inline_ids():
    cfg = IngestionConfig(min_block_length=10, max_block_length=100, dedup_enabled=False)
    blocks = [
        {"text": "First requirement string.", "inline_id": "IN-1"},
        {"text": "Second requirement string.", "inline_id": "IN-1"}
    ]
    
    reqs = normalise_blocks(blocks, cfg)
    assert reqs == {"IN-1": "First requirement string.", "IN-1_2": "Second requirement string."}

def test_normalise_blocks_whitespace():
    cfg = IngestionConfig(min_block_length=10, max_block_length=100, dedup_enabled=False)
    blocks = [{"text": "  Lots   of  \n spaces  "}]
    
    reqs = normalise_blocks(blocks, cfg)
    assert list(reqs.values())[0] == "Lots of spaces"

def test_normalise_blocks_length_filtering():
    cfg = IngestionConfig(min_block_length=10, max_block_length=20, dedup_enabled=False)
    blocks = [
        {"text": "Too short"},
        {"text": "This is a very long string that should be truncated to exactly twenty chars."}
    ]
    
    reqs = normalise_blocks(blocks, cfg)
    assert len(reqs) == 1
    val = list(reqs.values())[0]
    assert len(val) == 20
    assert val == "This is a very long "

def test_normalise_blocks_dedup():
    cfg = IngestionConfig(min_block_length=10, max_block_length=100, dedup_enabled=True)
    blocks = [
        {"text": "This is a requirement."},
        {"text": "This is a requirement."}
    ]
    
    reqs = normalise_blocks(blocks, cfg)
    assert len(reqs) == 1

def test_normalise_blocks_empty():
    cfg = IngestionConfig(min_block_length=10, max_block_length=100, dedup_enabled=False)
    blocks = [{"text": "short"}]
    
    with pytest.raises(EmptyRequirementsError):
        normalise_blocks(blocks, cfg)
