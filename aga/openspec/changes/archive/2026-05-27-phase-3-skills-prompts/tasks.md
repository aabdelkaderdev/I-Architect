## 1. Skills Bundle Setup

- [x] 1.1 Create `aga/Skills/SKILL.md` with YAML frontmatter (`name: c4-plantuml-syntax`, `description`, `metadata.version`, `metadata.target`) and a tag registry table mapping tags (`c4:rules`, `c4:context_example`, `c4:container_example`, `c4:component_example`) to reference file sections.
- [x] 1.2 Create `aga/Skills/references/c4.md` containing headed sections for C4 PlantUML syntax rules, element macros, relationship arrows, layout directives, and example diagrams (context, container, component).

## 2. Mustache Prompt Templates

- [x] 2.1 Create `aga/prompts/agent_instruction.md` with YAML frontmatter listing expected variables, a `{{! skill: c4:rules as c4_plantuml_rules }}` directive, and the system prompt body with `{{{c4_plantuml_rules}}}` and `{{variable}}` placeholders. The rendered output targets `create_agent(..., system_prompt=...)` or middleware `before_model`/`@dynamic_prompt`.
- [x] 2.2 Create `aga/prompts/code_generation.md` with skill tag `{{! skill: c4:rules as c4_rules }}`, focus entity variables, and `{{{elements_block}}}` / `{{{relationships_block}}}` triple-stache blocks.
- [x] 2.3 Create `aga/prompts/error_correction.md` with `{{{error_text}}}`, `{{{current_puml_code}}}`, `{{retry_count}}`, and `{{max_retries}}` variables (no skill injection needed).

## 3. Utility Loaders

- [x] 3.1 Create `aga/utils/__init__.py` exporting `load_prompt` and `load_skill_content`.
- [x] 3.2 Create `aga/utils/skill_loader.py` with function `load_skill_content(skill_dir, tag) -> str` that parses the SKILL.md frontmatter, resolves the tag to a reference file section, and returns the section content. Raises `KeyError` on unknown tags.
- [x] 3.3 Create `aga/utils/prompt_loader.py` with function `load_prompt(template_name, context) -> str` that reads the template from `aga/prompts/`, extracts `{{! skill: ... }}` directives, resolves each via `skill_loader`, merges skill content into the context dict, validates required variables from frontmatter, and renders via `chevron.render()`. Raises `ValueError` on missing variables.
