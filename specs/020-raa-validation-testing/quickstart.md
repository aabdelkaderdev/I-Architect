# Quickstart: Running the RAA Test Suite

## Prerequisites
Ensure that all dependencies are installed.

```bash
pip install pytest pytest-asyncio
```

## Running the Tests

To execute the full RAA test suite encompassing unit, integration, and functional checks:

```bash
pytest tests/raa/ -v
```

### Running Specific Categories

If you want to focus exclusively on functional compliance tests (e.g., C4 output structure checks):
```bash
pytest tests/raa/test_final_merge.py -v
```

To run unit tests specifically evaluating the Judge's entity deduplication and hierarchy validation:
```bash
pytest tests/raa/test_judge.py -v
```

## Creating Golden Fixtures

When updating the structural rules, you may need to update the golden JSON fixtures in `tests/raa/fixtures/`. Ensure that any manually constructed JSON files strictly respect the hierarchical `ArchModel` constraints defined in `RAA_Plan.md` §4.
