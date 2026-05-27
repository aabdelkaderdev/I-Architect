## 1. Directory Structure

- [x] 1.1 Create the `aga` module root directory.
- [x] 1.2 Create the top-level `__init__.py` file in `aga/`.
- [x] 1.3 Create the subdirectories: `Skills`, `graphs`, `nodes`, `prompts`, `state`, `tools`, and `utils`.
- [x] 1.4 Create `__init__.py` files in all the newly created subdirectories to mark them as packages.

## 2. Configuration

- [x] 2.1 Create `aga/state/config.py` and define `AGAConfig` as a Python `@dataclass` (from `dataclasses`). This will serve as the `context_schema` for `StateGraph`. Fields: `max_retries` (int, default 5), `plantuml_server_url` (str, default `"http://www.plantuml.com/plantuml"`), `checkpoint_db_path` (str, no default), `output_dir_png` (str, no default), `output_dir_puml` (str, no default), `output_dir_diagrams` (str, no default), `read_timeout_seconds` (int, default 30).

## 3. State Schemas

- [x] 3.1 Create `aga/state/schemas.py` and define the `AGAInput`, `AGAOutput`, and `AGAState` TypedDicts.
- [x] 3.2 For accumulator channels (`completed_diagrams`, `failed_diagrams`) in `AGAState`, use `Annotated[list[dict], operator.add]` reducer syntax (import `operator` and `Annotated` from `typing`).

## 4. Pydantic Models

- [x] 4.1 Create `aga/state/models.py`.
- [x] 4.2 Define internal state Pydantic models: `DiagramSpec`, `CompletedDiagram`, `FailedDiagram`, and `SessionReport`.
- [x] 4.3 Define input validation Pydantic models mapping to the flat JSON: `Entity`, `Relationship`, and `ArchModel` (do not use strict validation).
