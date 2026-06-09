import pytest
import json
from ingestion.extractors import extract_from_json
from ingestion.exceptions import NonStandardJSONError, FormatMismatchError

def test_extract_from_json_compliant(tmp_path):
    data = {"REQ-1": "This is a requirement.", "REQ-2": "This is another requirement."}
    p = tmp_path / "valid.json"
    p.write_text(json.dumps(data))
    
    result = extract_from_json(str(p))
    assert result == data

def test_extract_from_json_not_dict(tmp_path):
    data = ["REQ-1", "This is a requirement."]
    p = tmp_path / "list.json"
    p.write_text(json.dumps(data))
    
    with pytest.raises(NonStandardJSONError, match="Root value is not a dict"):
        extract_from_json(str(p))

def test_extract_from_json_nested(tmp_path):
    data = {"REQ-1": {"text": "This is a requirement."}}
    p = tmp_path / "nested.json"
    p.write_text(json.dumps(data))
    
    with pytest.raises(NonStandardJSONError, match="Keys and values must be non-empty strings"):
        extract_from_json(str(p))

def test_extract_from_json_empty_value(tmp_path):
    data = {"REQ-1": "  "}
    p = tmp_path / "empty_value.json"
    p.write_text(json.dumps(data))
    
    with pytest.raises(NonStandardJSONError, match="Keys and values must be non-empty strings"):
        extract_from_json(str(p))

def test_extract_from_json_invalid_json(tmp_path):
    p = tmp_path / "invalid.json"
    p.write_text("{invalid_json: true")
    
    with pytest.raises(FormatMismatchError, match="File cannot be parsed as JSON"):
        extract_from_json(str(p))
