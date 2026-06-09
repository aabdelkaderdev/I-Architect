import pytest
from unittest.mock import patch, MagicMock

from ingestion.extractors import (
    _clean_text,
    _process_table,
    _segment_text,
    extract_from_pdf
)
from ingestion.exceptions import ExtractionError, FormatMismatchError

def test_clean_text():
    # non-printable chars
    assert _clean_text("Hello\x00World") == "HelloWorld"
    # smart quotes
    assert _clean_text("It\u2019s a \u201ctest\u201d") == "It's a \"test\""

def test_process_table():
    # Semantic headers
    table1 = [
        ["ID", "Description"],
        ["REQ-1", "The system shall work"]
    ]
    blocks1 = _process_table(table1, page_num=1)
    assert len(blocks1) == 1
    assert blocks1[0]["text"] == "ID: REQ-1 | Description: The system shall work"
    assert blocks1[0]["source_page"] == 1
    
    # Non-semantic headers
    table2 = [
        ["A", "B"],
        ["Val1", "Val2"]
    ]
    blocks2 = _process_table(table2, page_num=2)
    assert len(blocks2) == 1
    assert blocks2[0]["text"] == "Val1 Val2"

def test_segment_text_list():
    text = "1. First item\n2. Second item\n• Bullet"
    blocks = _segment_text(text, page_num=1)
    assert len(blocks) == 3
    assert blocks[0]["text"] == "1. First item"
    assert blocks[1]["text"] == "2. Second item"
    assert blocks[2]["text"] == "• Bullet"

def test_segment_text_paragraph():
    text = "Para 1\n\nPara 2\n\nPara 3"
    blocks = _segment_text(text, page_num=1)
    assert len(blocks) == 3
    assert blocks[0]["text"] == "Para 1"
    
def test_segment_text_sentence_fallback():
    # >500 chars paragraph
    long_para = "A" * 501 + ". And a new sentence. And another."
    blocks = _segment_text(long_para, page_num=1)
    assert len(blocks) == 3
    assert blocks[0]["text"] == "A" * 501 + "."
    assert blocks[1]["text"] == "And a new sentence."
    assert blocks[2]["text"] == "And another."

@patch("ingestion.extractors.pdfplumber.open")
def test_extract_from_pdf_stripping(mock_open):
    mock_pdf = MagicMock()
    mock_page1 = MagicMock()
    mock_page2 = MagicMock()
    
    mock_page1.extract_text.return_value = "Confidential Header\nUnique text 1\nFooter"
    mock_page2.extract_text.return_value = "Confidential Header\nUnique text 2\nFooter"
    mock_page1.find_tables.return_value = []
    mock_page2.find_tables.return_value = []
    
    mock_pdf.pages = [mock_page1, mock_page2]
    mock_open.return_value.__enter__.return_value = mock_pdf
    
    blocks = extract_from_pdf("dummy.pdf", pdf_engine="pdfplumber", header_footer_threshold=0.6)
    texts = [b["text"] for b in blocks]
    
    assert "Confidential Header" not in texts
    assert "Footer" not in texts
    assert "Unique text 1" in texts
    assert "Unique text 2" in texts

@patch("ingestion.extractors.pdfplumber.open")
def test_extract_from_pdf_no_text(mock_open):
    mock_pdf = MagicMock()
    mock_page = MagicMock()
    mock_page.extract_text.return_value = ""
    mock_page.find_tables.return_value = []
    mock_pdf.pages = [mock_page]
    mock_open.return_value.__enter__.return_value = mock_pdf
    
    with pytest.raises(ExtractionError, match="No extractable text"):
        extract_from_pdf("dummy.pdf", pdf_engine="pdfplumber")

@patch("ingestion.extractors.pdfplumber.open")
def test_extract_from_pdf_corrupt(mock_open):
    mock_open.side_effect = Exception("corrupt file")
    with pytest.raises(FormatMismatchError, match="Could not parse as PDF"):
        extract_from_pdf("dummy.pdf", pdf_engine="pdfplumber")
