import os
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime

from ingestion.schema import IngestionState, IngestionContext
from ingestion.exceptions import (
    EmptyRequirementsError
)
from ingestion.format_router import format_router_node, route_by_format
from ingestion.extractors import (
    extract_from_pdf,
    extract_from_docx,
    extract_from_txt,
    extract_from_json,
)
from ingestion.normaliser import normalise_blocks
from ingestion.rfa import filter_requirements

def pdf_extractor_node(state: IngestionState) -> dict:
    cfg = state["ingestion_config"]
    file_path = state["file_path"]
    blocks = extract_from_pdf(
        file_path,
        pdf_engine=cfg.pdf_engine,
        header_footer_threshold=cfg.header_footer_threshold,
    )
    return {"extracted_blocks": blocks}

def docx_extractor_node(state: IngestionState) -> dict:
    file_path = state["file_path"]
    blocks = extract_from_docx(file_path)
    return {"extracted_blocks": blocks}

def txt_extractor_node(state: IngestionState) -> dict:
    cfg = state["ingestion_config"]
    file_path = state["file_path"]
    blocks = extract_from_txt(file_path, encoding_fallback=cfg.encoding_fallback)
    return {"extracted_blocks": blocks}

def json_validator_node(state: IngestionState) -> dict:
    file_path = state["file_path"]
    requirements = extract_from_json(file_path)
    return {"extracted_requirements": requirements}

def normaliser_node(state: IngestionState) -> dict:
    if "extracted_blocks" in state and state["extracted_blocks"]:
        cfg = state["ingestion_config"]
        blocks = state["extracted_blocks"]
        requirements = normalise_blocks(blocks, cfg)
        return {"extracted_requirements": requirements}
    return {}

def rfa_node(state: IngestionState, runtime: Runtime[IngestionContext]) -> dict:
    fcfg = state["filter_config"]
    if not fcfg.enabled:
        return {"extracted_requirements": state["extracted_requirements"], "filter_report": None}
        
    file_path = state["file_path"]
    _, ext = os.path.splitext(file_path.lower())
    
    # JSON passthrough rule: Compliant JSON bypasses filtering
    if ext == ".json" and fcfg.skip_filter_for_json:
        return {"extracted_requirements": state["extracted_requirements"], "filter_report": None}
        
    llm = runtime.context.llm
    filtered_requirements, report = filter_requirements(
        state["extracted_requirements"], 
        llm,
        confidence_threshold=fcfg.confidence_threshold,
        batch_size=fcfg.filter_batch_size,
        log_dropped=fcfg.log_dropped,
        emit_report=fcfg.emit_report
    )
    
    if not filtered_requirements:
        raise EmptyRequirementsError("All requirements were filtered out as noise.")
        
    return {"extracted_requirements": filtered_requirements, "filter_report": report}

def output_assembly_node(state: IngestionState) -> dict:
    reqs = state.get("extracted_requirements", {})
    if not reqs:
        raise EmptyRequirementsError("No requirements extracted from the file.")
    return {"extracted_requirements": reqs}

def build_ingestion_graph(db_path: str | None = None):
    """
    Builds and compiles the Data Ingestion & Requirement Filtering pipeline graph.
    """
    builder = StateGraph(IngestionState, context_schema=IngestionContext)
    
    builder.add_node("format_router", format_router_node)
    builder.add_node("pdf_extractor", pdf_extractor_node)
    builder.add_node("docx_extractor", docx_extractor_node)
    builder.add_node("txt_extractor", txt_extractor_node)
    builder.add_node("json_validator", json_validator_node)
    builder.add_node("normaliser", normaliser_node)
    builder.add_node("rfa", rfa_node)
    builder.add_node("output_assembly", output_assembly_node)
    
    builder.add_edge(START, "format_router")
    
    builder.add_conditional_edges(
        "format_router",
        route_by_format,
        {
            "pdf": "pdf_extractor",
            "docx": "docx_extractor",
            "txt": "txt_extractor",
            "json": "json_validator",
        }
    )
    
    for extractor in ["pdf_extractor", "docx_extractor", "txt_extractor", "json_validator"]:
        builder.add_edge(extractor, "normaliser")
        
    builder.add_edge("normaliser", "rfa")
    builder.add_edge("rfa", "output_assembly")
    builder.add_edge("output_assembly", END)
    
    if db_path:
        try:
            from langgraph.checkpoint.sqlite import SqliteSaver
            import sqlite3
            conn = sqlite3.connect(db_path, check_same_thread=False)
            saver = SqliteSaver(conn)
            return builder.compile(checkpointer=saver)
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Failed to initialize SqliteSaver with db_path={db_path}: {e}. Proceeding without checkpointer.")
            return builder.compile()
            
    return builder.compile()
