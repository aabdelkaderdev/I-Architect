---
name: c4-plantuml-syntax
description: Authoritative reference for generating C4 architecture diagrams (Context, Container, Component) using PlantUML. Covers C4-PlantUML includes, element types, relationship syntax, and diagram layout.
allowed-tools: Read, Glob, Grep
---

# C4 PlantUML Syntax Reference

## Overview

PlantUML is a Java-based tool that creates diagrams from text descriptions. This skill is scoped to **C4 model diagrams only** — the first three C4 levels used by the Architecture Generation Agent (AGA):

| C4 Level | Diagram | Purpose |
| --- | --- | --- |
| 1 — Context | System Context | Shows the system in its environment: users, external systems, high-level relationships |
| 2 — Container | Container | Shows the system's containers (applications, data stores, services) and their interactions |
| 3 — Component | Component | Shows the internal components of a single container and their relationships |

**Key advantages:**

- Mature C4 model integration via `C4-PlantUML` includes with icons/sprites
- Text-based — generated programmatically from RAA's C4-compliant JSON model
- Battle-tested (since 2009)

**Requirements:**

- Java Runtime Environment (JRE)
- GraphViz (for layout)
- Or use Docker: `docker run -p 8080:8080 plantuml/plantuml-server`

---

## Basic Syntax

All C4 PlantUML diagrams are wrapped in start/end tags with C4 includes:

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
' Or C4_Container.puml / C4_Component.puml

title My C4 Diagram Title
caption This is a caption

' Diagram content
@enduml
```

**Comments:**

- Single line: `' This is a comment`
- Block: `/' This is a block comment '/`

---

## References

For detailed C4 syntax and complete examples, see:

| Reference | Content | When to Load |
| --- | --- | --- |
| [c4.md](references/c4.md) | C4 context, container, component diagram syntax, element macros, relationship arrows, layout directives | Creating any C4 architecture diagram |

---

## File Extensions

| Extension | Description |
| --- | --- |
| `.puml` | Standard PlantUML file |
| `.plantuml` | Alternative extension |
| `.pu` | Short extension |
| `.iuml` | Include file |

---

## Test Scenarios

### Scenario 1: Creating a C4 System Context diagram

**Query:** "Create a C4 System Context diagram for the I-Architect platform"

**Expected:** Skill activates, provides C4_Context include, Person/System/System_Ext macros, and Rel arrows

### Scenario 2: Creating a C4 Container diagram

**Query:** "Create a C4 container diagram in PlantUML"

**Expected:** Skill activates, provides C4_Container include, Container/ContainerDb macros, and technology annotations

### Scenario 3: Creating a C4 Component diagram

**Query:** "Create a C4 component diagram for the RAA pipeline container"

**Expected:** Skill activates, provides C4_Component include, Component macros with technology labels, and directed relationships

---

**Last Updated:** 2026-05-15
**PlantUML Version:** 1.2024.6

## Version History

- **v2.0.0** (2026-05-15): Scoped to C4 diagrams only (Context, Container, Component). Removed non-C4 diagram types.
- **v1.1.0** (2025-12-28): Refactored to progressive disclosure - extracted content to references/
- **v1.0.0** (2025-12-26): Initial release
