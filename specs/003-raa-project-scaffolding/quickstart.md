# Quickstart: RAA Project Scaffolding

This guide describes how to work with the RAA project directory structure.

## 1. Navigating the Scaffolding

After creation, the directories serve two separate concerns:

1. **Design-Time Documents (`Skills/RAA/references/`)**:
   These are reference manuals (e.g., `C4.md`, `SAAM.md`) for developers and agents. They must remain human-readable and describe the *what* and *why* of the architecture decisions.

2. **Runtime Code and Prompts (`raa/`)**:
   This contains the executable python scripts (`raa/llm.py`, `raa/runner.py`) and prompt files (`raa/prompts/`).

## 2. Using Prompt Excerpts

Excerpts under `raa/prompts/excerpts/` are tagged text snippets used for dynamic prompt building:

### Tag-to-File Mapping (per RAA_Plan.md Section 21C)

| Node | Tags requested | File |
|------|---------------|------|
| Entity extraction | `c4:levels`, `c4:notation` | `c4_levels.txt`, `c4_notation.txt` |
| Relationship extraction | `c4:notation`, `c4:technology` | `c4_notation.txt`, `c4_technology.txt` |
| Pattern selection | `c4:levels` | `c4_levels.txt` |
| SAAM tradeoff (judge) | `saam:steps`, `saam:scenarios` | `saam_steps.txt`, `saam_scenarios.txt` |
| Final merge / reconciliation | `c4:levels`, `c4:notation`, `c4:technology` | `c4_levels.txt`, `c4_notation.txt`, `c4_technology.txt` |

- Nodes request specific snippets by tag name (e.g. `c4:levels` -> `c4_levels.txt`).
- Excerpt lengths are strictly capped at 25 words to keep LLM context usage low.
