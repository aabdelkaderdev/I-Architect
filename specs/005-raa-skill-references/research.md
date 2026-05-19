# Research Report: Skill Resource Reference Documents

This report documents layout decisions for the Skill Resource Bundle references under `Skills/RAA/references/`.

## 1. Document Separation & Scope

### Decision
Partition the documentation into:
1. **Authoritative References** (`C4.md`, `Quality_Attributes.md`): These cover static taxonomies and standard models. They do not have runtime inputs/outputs.
2. **Skill-Specific References** (`Entity_Extraction.md`, etc.): These cover step-by-step extraction rules, mapping heuristics, and edge cases. They correspond to specific subgraph node duties.

### Rationale
Splitting design-time definitions this way allows runtime prompt-builder code to load only the guidelines relevant to the current active node.

---

## 2. Headings and Validation Structure

### Decision
Enforce a strict seven-section heading outline for all skill-specific documents:
1. **Purpose**
2. **Input**
3. **Normative rules**
4. **Decision guidelines**
5. **Output schema**
6. **Error cases**
7. **Examples**

### Rationale
Using a predictable list of headings makes it easy to validate documentation completeness with simple scripts, ensuring no critical sections (like Output schema or Error cases) are left empty.
