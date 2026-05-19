# Test Data Models and Fixtures

Testing the RAA pipeline requires synthesizing data structures that mimic the output of the ARLO step. These are the primary fixtures needed for testing.

### Fixtures Needed

1. **`mock_arlo_output`**
   - Returns a valid `ARLOOutput` dictionary.
   - Includes 5 `asrs`, 10 `non_asr` items, 2 `condition_groups`, and simulated `quality_weights`.

2. **`mock_arch_fragment`**
   - Returns a simulated `ArchFragment` matching the schema defined in `RAA_Plan.md` §4.
   - Contains 1 system, 2 containers, 3 components, and varied relationships.
   - Used for testing the Judge merge logic without running the LLM generation nodes.

3. **`mock_sqlite_db`**
   - A fixture utilizing `tmp_path` to build an empty database schema matching `asr_embeddings.db`.
   - Used for testing the `preparation` node's capability to identify missing or stale records.

4. **`golden_c4_model`**
   - A static JSON file saved in `tests/raa/fixtures/golden_model.json`.
   - Represents the correct, 100% C4-compliant output for a known set of fragments. Used in functional tests.
