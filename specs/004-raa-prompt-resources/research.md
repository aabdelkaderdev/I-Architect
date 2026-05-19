# Research Report: Prompt Resource Format and Validation

This report documents formatting decisions for the RAA Prompt Resource Bundle.

## 1. File Formats and Directory Structure

### Decision
Store constraints in separate Markdown (`.md`) files and excerpts in separate Plain Text (`.txt`) files within `raa/prompts/`.

### Rationale
This approach allows:
1. Version-controlled readability (diffs are easy to read in PRs).
2. Straightforward file reads on-demand: a node needing the `c4:levels` tag can read `raa/prompts/excerpts/c4_levels.txt` directly without parsing a large structured config file.

### Alternatives Considered
- **Single YAML/JSON Bundle file**: Rejected because it requires parsing logic on every node run, and multi-line strings in JSON/YAML can be prone to escaping/formatting issues.

---

## 2. Word Count Validation Policy

### Decision
Implement a automated unit test check to count space-delimited words in each `.txt` file under `raa/prompts/excerpts/`.

### Rationale
Ensures that none of the excerpt files exceed the 25-word cap defined in `RAA_Plan.md` §2C. Keeping excerpts short preserves LLM context window space and focuses the agent on core constraints.
