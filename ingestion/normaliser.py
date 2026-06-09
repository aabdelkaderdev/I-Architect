import logging
from ingestion.exceptions import EmptyRequirementsError
from ingestion.schema import IngestionConfig

logger = logging.getLogger(__name__)

def normalise_blocks(blocks: list[dict], config: IngestionConfig) -> dict[str, str]:
    """
    Normalises raw text blocks into the standard requirement format by assigning IDs,
    stripping whitespace, filtering lengths, and deduplicating.
    """
    requirements = {}
    seen_blocks = set()
    current_id = 1
    
    inline_id_counts = {}

    for block in blocks:
        raw_text = block.get("text", "")
        # Whitespace normalisation
        norm_block = " ".join(raw_text.split())
        
        if len(norm_block) < config.min_block_length:
            continue
            
        if len(norm_block) > config.max_block_length:
            norm_block = norm_block[:config.max_block_length]
            
        if config.dedup_enabled:
            if norm_block in seen_blocks:
                logger.warning(f"Dropped duplicate block: {norm_block[:30]}...")
                continue
            seen_blocks.add(norm_block)
            
        inline_id = block.get("inline_id")
        if inline_id:
            # Handle inline ID uniqueness
            if inline_id in inline_id_counts:
                inline_id_counts[inline_id] += 1
                req_id = f"{inline_id}_{inline_id_counts[inline_id]}"
                logger.warning(f"Duplicate inline ID '{inline_id}' found, appending suffix -> {req_id}")
            else:
                inline_id_counts[inline_id] = 1
                req_id = inline_id
        else:
            req_id = f"{config.id_prefix}{current_id}"
            current_id += 1
            
        requirements[req_id] = norm_block
        
    if not requirements:
        raise EmptyRequirementsError("Final requirement set contains zero entries.")
        
    return requirements
