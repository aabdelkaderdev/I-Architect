from dataclasses import dataclass
from typing import Literal
from typing_extensions import TypedDict, NotRequired
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, Field

class FilteredRequirement(BaseModel):
    """Represents the classification result for a single requirement."""
    id: str = Field(description="The requirement ID, exactly as provided in the input batch.")
    classification: Literal["SIGNAL", "NOISE"] = Field(description="Classification of the requirement as either SIGNAL or NOISE.")
    confidence: float = Field(ge=0.0, le=1.0, description="The LLM's confidence in its classification, range 0.0-1.0.")
    reason: str = Field(description="A one-sentence justification for the classification. For Noise, identifies which noise category the entry matches. For Signal, identifies which signal category applies.")

class FilterBatch(BaseModel):
    """Represents the classification result for an entire batch."""
    requirements: list[FilteredRequirement] = Field(description="All classified requirements in the batch. Must contain exactly one entry per input requirement.")

class DroppedRequirement(TypedDict):
    """Details of a requirement dropped by the RFA."""
    id: str
    original_text: str
    confidence: float
    reason: str

class KeptNoiseRequirement(TypedDict):
    """Details of a requirement classified as noise but kept due to low confidence."""
    id: str
    original_text: str
    confidence: float
    reason: str

class FilterReport(TypedDict):
    """Structured report of RFA filtering results."""
    total_input: int
    total_signal: int
    total_noise_dropped: int
    total_noise_kept: int
    confidence_threshold: float
    dropped_requirements: list[DroppedRequirement]
    noise_kept_below_threshold: list[KeptNoiseRequirement]



@dataclass
class IngestionConfig:
    """
    Controls Stage 1: extraction and normalisation.
    """
    id_prefix: str = "REQ-"
    min_block_length: int = 15
    max_block_length: int = 2000
    dedup_enabled: bool = True
    encoding_fallback: str = "utf-8"
    pdf_engine: str = "pdfplumber"
    header_footer_threshold: float = 0.6

@dataclass
class FilterConfig:
    """
    Controls Stage 2: the Requirement Filtering Agent (RFA).
    """
    enabled: bool = True
    confidence_threshold: float = 0.7
    filter_batch_size: int = 20
    log_dropped: bool = True
    emit_report: bool = True
    skip_filter_for_json: bool = True

class IngestionState(TypedDict):
    """
    State schema for the Ingestion pipeline.
    
    Attributes:
        file_path: Absolute path to the uploaded file.
        extracted_requirements: The final clean requirement set (keys: IDs, values: text).
        ingestion_config: Configuration for Stage 1 (extraction and normalisation).
        filter_config: Configuration for Stage 2 (Requirement Filtering Agent).
        filter_report: Structured report from the RFA node.
    """
    file_path: str
    file_format: NotRequired[str]
    extracted_blocks: NotRequired[list[dict]]
    extracted_requirements: dict[str, str]
    ingestion_config: IngestionConfig
    filter_config: FilterConfig
    filter_report: NotRequired[dict | None]

@dataclass
class IngestionContext:
    """
    Runtime context for the Ingestion pipeline.
    
    Attributes:
        llm: A BaseChatModel instance to be used by the RFA for classification.
    """
    llm: BaseChatModel
