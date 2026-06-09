import re
from ingestion.schema import IngestionConfig, FilterConfig

def validate_ingestion_config(cfg: IngestionConfig) -> None:
    """
    Validates the IngestionConfig fields according to business rules.
    Raises ValueError if any field is invalid.
    """
    if not cfg.id_prefix:
        raise ValueError("id_prefix cannot be empty.")
    if not re.match(r"^[A-Za-z\-]+-$", cfg.id_prefix):
        raise ValueError("id_prefix must contain only alphabetic characters and hyphens, and must end with a hyphen.")
        
    if cfg.min_block_length < 1:
        raise ValueError("min_block_length must be >= 1.")
    if cfg.min_block_length >= cfg.max_block_length:
        raise ValueError("min_block_length must be strictly less than max_block_length.")
        
    if cfg.header_footer_threshold < 0.0 or cfg.header_footer_threshold > 1.0:
        raise ValueError("header_footer_threshold must be between 0.0 and 1.0.")
        
    if cfg.pdf_engine not in ("pdfplumber", "pymupdf"):
        raise ValueError("pdf_engine must be 'pdfplumber' or 'pymupdf'.")

def validate_filter_config(cfg: FilterConfig) -> None:
    """
    Validates the FilterConfig fields according to business rules.
    Raises ValueError if any field is invalid.
    """
    if cfg.confidence_threshold < 0.0 or cfg.confidence_threshold > 1.0:
        raise ValueError("confidence_threshold must be between 0.0 and 1.0.")
        
    if cfg.filter_batch_size < 1:
        raise ValueError("filter_batch_size must be >= 1.")
