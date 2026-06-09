from typing import Tuple, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models import BaseChatModel
from pydantic import ValidationError
from pathlib import Path
import logging
import json
from ingestion.schema import FilterBatch, FilterReport, DroppedRequirement, KeptNoiseRequirement

logger = logging.getLogger(__name__)

def _classify_batch(batch_json: str, system_prompt: str, llm: BaseChatModel) -> FilterBatch:
    from langchain_core.messages import SystemMessage, HumanMessage
    chain = llm.with_structured_output(FilterBatch).with_retry(stop_after_attempt=3)
    return chain.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=batch_json)
    ])

def filter_requirements(
    requirements: dict[str, str], 
    llm: BaseChatModel,
    confidence_threshold: float,
    batch_size: int,
    log_dropped: bool,
    emit_report: bool
) -> Tuple[dict[str, str], Optional[FilterReport]]:
    """
    Requirement Filtering Agent (RFA).
    Filters out noise from the requirements using the provided LLM.
    """
    filtered_requirements = {}
    
    total_input = len(requirements)
    total_signal = 0
    total_noise_dropped = 0
    total_noise_kept = 0
    dropped_requirements_list: list[DroppedRequirement] = []
    noise_kept_below_threshold: list[KeptNoiseRequirement] = []
    
    # Load prompt at invocation time
    prompt_path = Path(__file__).parent / "prompts" / "filter_classification.md"
    try:
        system_prompt = prompt_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.error(f"Prompt file not found at {prompt_path}")
        raise
        
    req_items = list(requirements.items())
    
    for i in range(0, len(req_items), batch_size):
        batch_items = req_items[i:i + batch_size]
        batch_json = json.dumps([{"id": req_id, "text": text} for req_id, text in batch_items])
        
        try:
            response: FilterBatch = _classify_batch(batch_json, system_prompt, llm)
        except ValidationError as e:
            logger.error("LLM failed to produce valid structured output after retries.", exc_info=True)
            raise
            
        for req in response.requirements:
            original_text = requirements.get(req.id, "")
            if req.classification == "SIGNAL":
                filtered_requirements[req.id] = original_text
                total_signal += 1
            elif req.classification == "NOISE":
                if req.confidence >= confidence_threshold:
                    if log_dropped:
                        logger.warning(f"Dropped requirement {req.id} (Confidence {req.confidence}): {req.reason}")
                    dropped_requirements_list.append({
                        "id": req.id,
                        "original_text": original_text,
                        "confidence": req.confidence,
                        "reason": req.reason
                    })
                    total_noise_dropped += 1
                else:
                    filtered_requirements[req.id] = original_text
                    noise_kept_below_threshold.append({
                        "id": req.id,
                        "original_text": original_text,
                        "confidence": req.confidence,
                        "reason": req.reason
                    })
                    total_noise_kept += 1
            
    report = None
    if emit_report:
        report = FilterReport(
            total_input=total_input,
            total_signal=total_signal,
            total_noise_dropped=total_noise_dropped,
            total_noise_kept=total_noise_kept,
            confidence_threshold=confidence_threshold,
            dropped_requirements=dropped_requirements_list,
            noise_kept_below_threshold=noise_kept_below_threshold
        )

    return filtered_requirements, report

