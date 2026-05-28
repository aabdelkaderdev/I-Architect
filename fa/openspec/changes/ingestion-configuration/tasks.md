# Tasks: Ingestion Configuration Dataclasses

## 1. Create Configuration Dataclasses

- `[x]` Create `IngestionConfig` as a `@dataclass` with all 7 fields, defaults, and
  docstrings explaining governance scope. Place in `ingestion/schema.py`.
- `[x]` Create `FilterConfig` as a `@dataclass` with all 6 fields, defaults, and
  docstrings. Place in `ingestion/schema.py`.

## 2. Update `IngestionState` TypedDict

- `[x]` Add `ingestion_config: IngestionConfig` channel to `IngestionState`.
- `[x]` Add `filter_config: FilterConfig` channel to `IngestionState`.
- `[x]` Verify `IngestionContext` (runtime context with `llm: BaseChatModel`) is
  unchanged — it stays as `context_schema` on `StateGraph`, passed at invocation via
  `context=IngestionContext(llm=...)`.

## 3. Wire Config Into Nodes

- `[x]` Update `data_ingestion_node` in `graph.py` to read `state["ingestion_config"]`
  instead of hardcoded defaults (e.g. pass `cfg.pdf_engine` to the PDF extractor,
  `cfg.encoding_fallback` to the TXT extractor).
- `[x]` Update `rfa_node` in `graph.py` to read `state["filter_config"]`:
  - Check `fcfg.enabled` — if `False`, skip filtering.
  - Check `fcfg.skip_filter_for_json` before JSON bypass.
  - Pass `fcfg.confidence_threshold` and `fcfg.filter_batch_size` to `filter_requirements`.
- `[x]` Update `normaliser.py` → `generate_ids_for_blocks` to accept `IngestionConfig`
  for `id_prefix`, `min_block_length`, `max_block_length`, and `dedup_enabled`.

## 4. Implement Validation (orchestrator-side helper)

- `[x]` Write `validate_ingestion_config(cfg: IngestionConfig)` that raises
  `ValueError` for invalid values per the rules in the PRD.
- `[x]` Write `validate_filter_config(cfg: FilterConfig)` similarly.
- `[x]` Ensure validation runs before `graph.invoke()` — place helpers in a
  `ingestion/validation.py` or equivalent.

## 5. Update Graph Invocation

- `[x]` Ensure `build_ingestion_graph()` still uses
  `StateGraph(IngestionState, context_schema=IngestionContext)`.
- `[x]` Update invocation callsite to pass config via state input:
  ```python
  graph.invoke(
      {"file_path": path, "ingestion_config": IngestionConfig(), "filter_config": FilterConfig()},
      context=IngestionContext(llm=llm),
  )
  ```
