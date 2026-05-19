# Research Report: Batch Queue Ordering and Risk Weights

This report documents the scoring system and tie-breaking logic.

## 1. Risk Value Mappings

### Decision
For the default `risk_first` strategy, quality attribute categories are assigned the following risk priority scores:
- **Security**: 4
- **Reliability**: 3
- **Performance**: 2
- **Usability**: 1
- **Others / General**: 0

The batch risk score is defined as the maximum risk score among its containing ASR requirements:
$$\text{Score}_{\text{batch}} = \max_{r \in \text{ASRs}} \text{Risk}(r)$$

### Rationale
Assigning the maximum value ensures that batches containing critical security or reliability concerns are treated with high priority, even if they also contain lower-priority usability items. Average values would dilute these critical flags.

---

## 2. Deterministic Tie-Breaking

### Decision
If two batches achieve equal sorting scores, the sort key will include a secondary item: the lexicographical comparison of the condition group IDs (e.g. `(score, group_id)`).

### Rationale
This prevents the queue sequence from being dependent on database retrieval orders or memory addresses, guaranteeing 100% deterministic pipeline routing.
