# Prompt Injection Contract

The prompt retrieval utility must strictly return the contents of the `.txt` files under `raa/prompts/excerpts/`.
It must raise `FileNotFoundError` if a requested tag translates to a missing file path.
It must only load the specified tag excerpts, keeping the LLM system prompt context size clean and compact.
The node-to-tag dictionary must match Section 21C constraints.
