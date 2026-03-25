# Celery Task & ETA Management — Functional & Non-Functional Requirements

> **Version:** 1.0
> **Source Plan:** `requirements_planning/4_orchestrator/celery_task_management_plan.md`
> **SRS Reference:** I-Architect SRS v2.3
> **Date:** 2026-03-24

---

## 1. Functional Requirements (FR)

### FR-TASK-001: Redis Distributed Lock for Concurrency Control
- **Description:** Before dispatching a Celery task, the system SHALL attempt to acquire a Redis distributed lock keyed as `lock:project:{project_id}`. If the key already exists, the API SHALL reject the request with HTTP `409 Conflict`. The UI-facing Project State Manager translates this into `423 Locked` for the Streamlit frontend.
- **SRS Trace:** §10.1, §1.1
- **Priority:** Must
- **Acceptance Criteria:** Two simultaneous pipeline run requests on the same project result in exactly one task dispatched and one `409/423` rejection.

### FR-TASK-002: Lock Scope Across Workflows
- **Description:** Workflows 1, 2, and 3 SHALL all use the same locking mechanism. Parallel sub-tasks within a single workflow (e.g., 3 parallel RAA instances in Workflow 3) SHALL run within a single parent project lock — they do NOT require individual locks.
- **SRS Trace:** §10.1
- **Priority:** Must
- **Acceptance Criteria:** In Workflow 3, three parallel RAA sub-tasks execute concurrently under one project lock; no internal lock contention occurs.

### FR-TASK-003: Lock Release in Finally Block
- **Description:** The project lock SHALL be released strictly within a `finally` block of the Celery task (or via a cleanup signal handler) to prevent deadlocks in case of task exceptions or crashes.
- **SRS Trace:** §10.1
- **Priority:** Must
- **Acceptance Criteria:** After a task fails with an unhandled exception, the Redis lock key is deleted and a subsequent run can be started immediately.

### FR-TASK-004: ARLO Batch Processing
- **Description:** ARLO SHALL ingest requirements in configurable batches (default: 10 requirements per batch). The batch size SHALL be adjustable via configuration.
- **SRS Trace:** §10.2, §1.11
- **Priority:** Must
- **Acceptance Criteria:** ARLO processes a set of 50 requirements in exactly 5 batches of 10 (default configuration).

### FR-TASK-005: ARLO Progress Emission
- **Description:** After each ARLO batch completes, the task SHALL update the Redis hash `meta:task:{task_id}` with:
  - `completed_batches` (integer)
  - `avg_batch_time` (float, rolling average of last 5 batches)
  - `progress_percent` (integer, 0–100)
- **SRS Trace:** §10.2
- **Priority:** Must
- **Acceptance Criteria:** After processing batch 3 of 5, `meta:task:{id}` contains `completed_batches=3`, `progress_percent=60`, and `avg_batch_time` reflecting the rolling average of up to 3 completed batches.

### FR-TASK-006: ETA Calculation (ARLO Only)
- **Description:** The Orchestrator SHALL calculate ETA for ARLO using the formula: `ETA_seconds = (total_batches - completed_batches) × avg_batch_time_seconds`, where `avg_batch_time_seconds` is a rolling average of the last 5 completed batches.
- **SRS Trace:** §10.2
- **Priority:** Must
- **Acceptance Criteria:** The ETA value displayed in the UI decreases monotonically as batches complete and reflects recent batch durations rather than the overall average.

### FR-TASK-007: Non-ARLO Agent Step Reporting
- **Description:** Non-ARLO agents (RAA, AGA, SA) SHALL NOT calculate ETA. They SHALL report qualitative status strings to the `meta:task:{id}` hash (e.g., `"Generating PlantUML..."`, `"Scoring Architecture..."`, `"Analyzing Requirements..."`).
- **SRS Trace:** §10.2
- **Priority:** Must
- **Acceptance Criteria:** The Progress Overlay displays the current phase label (e.g., "Generating PlantUML...") for non-ARLO agents without an ETA countdown.

### FR-TASK-008: Graceful Cancellation (Soft Kill)
- **Description:** The "Cancel Run" button SHALL set a Redis key `cancel:task:{task_id} = True`. Celery SHALL NOT receive a `SIGTERM`. Every LangGraph node and the ARLO batch loop SHALL check for the cancellation token at the start of each execution cycle.
- **SRS Trace:** §10.1, §1.11
- **Priority:** Must
- **Acceptance Criteria:** Pressing "Cancel Run" during batch 3 of 5 results in the current batch completing, the agent saving its checkpoint, the task status transitioning to `CANCELLED`, and the project lock being released.

### FR-TASK-009: Checkpoint Save on Cancellation
- **Description:** Upon detecting a cancellation token, the running agent SHALL save the current LangGraph checkpoint, mark the run as `CANCELLED` in the database, and exit cleanly.
- **SRS Trace:** §10.3
- **Priority:** Must
- **Acceptance Criteria:** After cancellation, a valid LangGraph checkpoint exists in `agent_states/` and the task record shows `status=CANCELLED`.

### FR-TASK-010: Success Result Persistence
- **Description:** Upon `SUCCESS`, the Celery task SHALL write the final artifact locations (file paths to output JSON/PDFs/TOONs) into the Django PostgreSQL database, not just Redis.
- **SRS Trace:** §10.1
- **Priority:** Must
- **Acceptance Criteria:** After task success, the Django ORM query for the task record returns the full list of generated artifact file paths.

### FR-TASK-011: Failure Error Logging
- **Description:** Upon `FAILURE` (unhandled exception), the task SHALL extract the full stack trace and write it to `meta:task:{task_id}` → `error_log` field in Redis for UI display.
- **SRS Trace:** §10.1
- **Priority:** Must
- **Acceptance Criteria:** After a task failure, the UI displays the specific error message and stack trace from the `error_log` field.

### FR-TASK-012: SSE Progress Streaming to Streamlit
- **Description:** The Django API SHALL stream progress updates to Streamlit via Server-Sent Events (SSE) using `StreamingHttpResponse`. The SSE endpoint `GET /api/tasks/{task_id}/progress/` SHALL emit events every 2 seconds containing `{eta_seconds, percent_complete, current_phase, status}`.
- **SRS Trace:** §10.2
- **Priority:** Must
- **Acceptance Criteria:** The Streamlit UI's `st.empty()` container updates the progress bar, ETA text, and phase label every 2 seconds without WebSocket dependencies.

### FR-TASK-013: Task Submission API
- **Description:** The system SHALL expose `POST /api/run/{workflow_type}/` that: (1) checks the project lock, (2) acquires the lock, (3) dispatches the Celery task, and (4) returns the `task_id` in a `202 Accepted` response.
- **SRS Trace:** §10.1, §10.2
- **Priority:** Must
- **Acceptance Criteria:** A valid POST returns `202` with a `task_id`; the Celery task is queued within 500ms.

### FR-TASK-014: Task Status API
- **Description:** The system SHALL expose `GET /api/status/{task_id}/` that reads `meta:task:{id}` from Redis and returns JSON with progress, logs, and status (`RUNNING`/`COMPLETED`/`FAILED`/`CANCELLED`).
- **SRS Trace:** §10.2
- **Priority:** Must
- **Acceptance Criteria:** Polling the status endpoint during a running task returns the correct progress percentage and phase.

### FR-TASK-015: Task Cancellation API
- **Description:** The system SHALL expose `POST /api/cancel/{task_id}/` that sets the `cancel:task:{task_id}` Redis key to `True`.
- **SRS Trace:** §10.1
- **Priority:** Must
- **Acceptance Criteria:** After calling the cancel endpoint, the running task detects the cancellation token within one batch cycle and exits gracefully.

---

## 2. Non-Functional Requirements (NFR)

### NFR-TASK-001: Redis Availability Resilience
- **Description:** The system SHALL auto-reconnect to Redis on startup. If Redis loses persistence (AOF/RDB), running tasks will fail but the system SHALL recover upon Redis availability restoration.
- **SRS Trace:** §10.1
- **Metric:** System auto-reconnects to Redis within 5 seconds of availability restoration.

### NFR-TASK-002: Polling Overhead Optimization
- **Description:** The `meta:task:{id}` Redis hash SHALL be optimized for high-frequency reads (every 2 seconds per active UI session) without performance degradation.
- **SRS Trace:** §10.2
- **Metric:** Redis hash read latency ≤ 1ms at P99 under 10 concurrent polling sessions.

### NFR-TASK-003: Lock Expiry Safety Valve
- **Description:** The lock key `lock:project:{project_id}` SHALL have a hard TTL of 2 hours. This prevents permanent project lockout in the event of a worker crash (OOM kill, SIGKILL) where the `finally` block cannot execute.
- **SRS Trace:** §10.1
- **Metric:** After simulated OOM kill, the lock auto-expires after exactly 2 hours.

### NFR-TASK-004: Task Result Retention
- **Description:** Task results in Redis SHALL have a TTL of 24 hours, allowing users to disconnect and return hours later to see the "Run Complete" state and logs.
- **SRS Trace:** §10.1
- **Metric:** Task metadata remains accessible for 24 hours after task completion.

### NFR-TASK-005: Ephemeral Progress TTL
- **Description:** Ephemeral progress data in Redis (batch-level updates) SHALL have a TTL of 1 hour after the last update, preventing stale progress data from accumulating.
- **SRS Trace:** §10.2
- **Metric:** Progress keys expire 1 hour after the last write, regardless of task status.

### NFR-TASK-006: Internal Retry Delegation
- **Description:** Retries for failed LLM API calls SHALL be handled internally by LangGraph nodes. Celery SHALL NOT retry the entire task graph on a single node failure.
- **SRS Trace:** §10.1
- **Metric:** A single LLM timeout within an agent node triggers node-level retry (up to 3 attempts) without restarting the entire Celery task.

---

## 3. Interface Requirements (IR)

### IR-TASK-001: Redis Key Schema
| Key Pattern | Type | Purpose | TTL |
|:--|:--|:--|:--|
| `lock:project:{project_id}` | String | Prevents concurrent runs on same project | 2 hours |
| `cancel:task:{task_id}` | Boolean | Signal for graceful task termination | 1 hour |
| `meta:task:{task_id}` | Hash | Stores `progress_percent`, `current_step`, `eta_seconds`, `error_log` | 24 hours |
| `celery-task-meta-{task_id}` | String | Native Celery state (PENDING, STARTED, SUCCESS, FAILURE) | 24 hours |

### IR-TASK-002: REST API Endpoints
| Method | Endpoint | Behavior |
|:--|:--|:--|
| `POST` | `/api/run/{workflow_type}/` | Check Lock → Set Lock → Dispatch Task → Return `task_id` (202) |
| `GET` | `/api/status/{task_id}/` | Read `meta:task:{id}` from Redis → Return progress JSON |
| `GET` | `/api/tasks/{task_id}/progress/` | SSE stream of progress events (every 2s) |
| `POST` | `/api/cancel/{task_id}/` | Set `cancel:task:{id}` key in Redis |

### IR-TASK-003: SSE Event Schema
```json
{
  "eta_seconds": 45,
  "percent_complete": 60,
  "current_phase": "ARLO - Processing Batch 3/5",
  "status": "RUNNING"
}
```

---

## 4. Disaster Recovery Requirements (DR)

### DR-TASK-001: Worker Crash Lock Recovery
- **Failure Mode:** Celery worker process is killed (OOM, SIGKILL) before the `finally` block releases the project lock.
- **Recovery Action:** The Redis lock auto-expires after its 2-hour TTL. For faster recovery, an admin endpoint `POST /api/admin/force-unlock/{project_id}/` may be provided.
- **SRS Trace:** §13

### DR-TASK-002: Redis Connection Failure
- **Failure Mode:** Redis becomes temporarily unavailable during a pipeline run.
- **Recovery Action:** The Celery worker detects the connection failure, logs the error, and transitions the task to `FAILURE` state. The lock is released on reconnection (or via TTL expiry). The UI displays a blocking modal.
- **User-Facing Message:** 🛑 *"The task management service lost connection. The current pipeline run has been stopped. Please retry."*
- **SRS Trace:** §13

### DR-TASK-003: Task State Loss Recovery
- **Failure Mode:** Redis persistence is lost (AOF/RDB failure), causing loss of task metadata.
- **Recovery Action:** The Django PostgreSQL database serves as the secondary source of truth for completed task results (via FR-TASK-010). The UI falls back to querying the database if Redis returns no data for a known `task_id`.
- **SRS Trace:** §13

---

*End of Celery Task Management Requirements Document*
