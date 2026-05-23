---
title: Product Brief: Requirements Analysis Agent (RAA)
status: draft
created: 2026-05-22
updated: 2026-05-22
---

# Product Brief: Requirements Analysis Agent (RAA)

## Executive Summary
The **Requirements Analysis Agent (RAA)** is a core agent module in the "I-Architect" diagram generation pipeline. It acts as the critical bridge between the upstream requirement locator (ARLO) and the downstream diagram renderer (AGA). RAA's mission is to ingest raw, classified requirements (ASR and non-ASR) and transform them into a C4-compliant, strictly nested JSON architecture model. 

By leveraging a batch-sequential, strategy-parallel LangGraph pipeline, RAA resolves structural representation challenges. The module executes three parallel extraction strategies, reconciles their outputs through an automated Judge, and prompts human architects for feedback on strategic trade-offs before generating the final model. RAA ensures 100% requirements traceability and eliminates layout duplicates, laying the foundation for enterprise-grade automated system design.

## The Problem
Prior attempts at automated C4 diagram generation suffered from three primary failures highlighted in the SAAM Audit:
1. **Container & Component Duplication**: Merging multiple independent LLM extraction runs without semantic deduplication inflated entity counts by over 40% (producing 35 containers instead of the actual 25). This created cluttered, unreadable diagrams.
2. **Low Requirements Traceability (50% Coverage Gap)**: Legacy extraction pipelines silently dropped phone-book style requirements, leaving 25 out of 50 requirements unmapped to any concrete structural boundary component.
3. **CQRS Violation**: Semantic deduplicators frequently merged distinct write and read databases into a single entity, violating architectural intent.

## The Solution
RAA introduces an **8-Phase LangGraph pipeline** that processes requirements in condition-anchored batches:
* **Preparation & Vector Cache**: Normalizes incoming requirements and caches 1024-dimensional FastEmbed vector embeddings in SQLite.
* **Batching & Bridging**: Groups ASRs with near-neighbor non-ASRs and injects overlap bridge requirements to maintain cross-batch continuity.
* **Strategy-Parallel Extraction**: Concurrently runs three distinct subgraphs—**SAAM-First** (scenario-driven), **Pattern-Driven** (matrix-guided), and **Entity-Driven** (bottom-up)—persisting state via concurrent SQLite WAL checkpoints.
* **Judge Reconciliation & Deduplication**: Reconciles the fragments, performs semantic deduplication using a conservative threshold, promotes cross-cutting concerns (e.g. security policies) to concrete components, and scores entity completeness.
* **Human-in-the-Loop Interrupt Gate**: Suspends execution in `interactive` mode to prompt architects for strategic resolutions, while bypassing interrupts with pre-computed suggestions in `autonomous` mode.
* **Residual Decision Ladder**: Evaluates leftover requirements sequentially to either enrich matching containers, propose new components, or track them as explicit coverage gaps.

## What Makes This Different
* **Bimodal Deduplication & Boundary Grouping**: To prevent CQRS violations, entities with similarity $\ge 0.80$ are merged, while moderate similarity ($0.60$ to $0.80$) triggers logical **C4 boundary groupings** on the canvas instead of destructive merging.
* **Annotation-to-Component Promotion**: Infrastructure policies (e.g., global TLS constraints) are promoted to first-class enforcement containers rather than repeating annotations across hundreds of arrows.
* **Strict Metamodel Constraints**: Deterministic tree assembly prevents orphan containers and validates all endpoint relationship scopes before handoff.
* `[ASSUMPTION: The downstream Architecture Generation Agent (AGA) will traverse the diagram manifest sequentially without performing any independent filtering, layout discovery, or edge-crossing optimization.]`

## Who This Serves
* **Devin (Pipeline Engineer)**: Needs a resilient, crash-safe middle stage that handles unstructured LLM outputs, executes fast caching, and provides clear metamodel validation.
* **Alex (Lead Architect)**: Wants to review high-context design decisions without diagram clutter, duplicate containers, or unresolvable layout orphans.

## Success Criteria
* **SM-1 (100% Requirements Accounting)**: Zero requirements silently dropped. Every input ID must map to a batch, a structural element, or an explicit coverage gap open question.
* **SM-2 (Deduplication Precision)**: Container duplication rate must remain **< 5%** in regression testing.
* **SM-C1 (CQRS Boundary Integrity)**: Zero mistakenly consolidated read/write datastores.
* **SM-3 (Checkpoint Integrity)**: **100%** successful graph recovery from the last completed batch checkpoint in case of execution failure.

## Scope
### In Scope (MVP)
* Full 8-Phase sequential LangGraph orchestrator.
* SQLite text-hash cached embedding generation using `mixedbread-ai/mxbai-embed-large-v1` via FastEmbed.
* Concurrent WAL-enabled SQLite checkpointing.
* Integration with the static quality-architecture `matrix.json`.
* Interactive interrupt gate with a `review_timeout_seconds` fallback.
* Residual requirements ladder with mandatory per-requirement decisions.

### Out of Scope (MVP)
* Dynamic reloading or runtime editing of the `matrix.json` parameters.
* A GUI dashboard for resolving open questions (Alex will interact via CLI or text file updates).
* `[ASSUMPTION: FastEmbed model files will be pre-cached inside the '../models' directory by the orchestrator environment setup script; RAA will not attempt to fetch model binaries over the network.]`

## Vision
Over the next 2-3 years, RAA will evolve from a batch-sequential text processor into a multi-agent architectural synthesizer. It will support collaborative review streams where multiple architects can resolve conflicts concurrently, dynamic matrix recalibration based on downstream testing logs, and proactive feedback integration that learns from past human resolutions to improve automatic Judge suggestions.
