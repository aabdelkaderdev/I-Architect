import pytest
from ingestion.extractors import extract_from_txt
from ingestion.exceptions import ExtractionError, FormatMismatchError

def test_extract_from_txt_structured(tmp_path):
    content = "REQ-1: First requirement\nREQ-2: Second requirement\nNot a requirement"
    file_path = tmp_path / "test_struct.txt"
    file_path.write_text(content, encoding="utf-8")
    
    blocks = extract_from_txt(str(file_path))
    assert len(blocks) == 2
    assert blocks[0]["text"] == "REQ-1: First requirement"
    assert blocks[1]["text"] == "REQ-2: Second requirement"

def test_extract_from_txt_unstructured_line_mode(tmp_path):
    content = "This is a short line.\nThis is another short line.\n"
    file_path = tmp_path / "test_unstruct_line.txt"
    file_path.write_text(content, encoding="utf-8")
    
    blocks = extract_from_txt(str(file_path))
    assert len(blocks) == 2
    assert blocks[0]["text"] == "This is a short line."
    
def test_extract_from_txt_unstructured_para_mode(tmp_path):
    long_line = "A" * 250
    content = f"{long_line}\n\nAnother paragraph {long_line}"
    file_path = tmp_path / "test_unstruct_para.txt"
    file_path.write_text(content, encoding="utf-8")
    
    blocks = extract_from_txt(str(file_path))
    assert len(blocks) == 2
    assert blocks[0]["text"] == long_line
    
def test_extract_from_txt_empty(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("   \n  ", encoding="utf-8")
    
    with pytest.raises(ExtractionError, match="No text content found"):
        extract_from_txt(str(file_path))
        
def test_extract_from_txt_encoding(tmp_path):
    content = "Requisito con acento: áéíóú\nMore text here"
    file_path = tmp_path / "encoded.txt"
    file_path.write_bytes(content.encode("iso-8859-1"))
    
    blocks = extract_from_txt(str(file_path))
    assert len(blocks) == 2
    assert "áéíóú" in blocks[0]["text"]
