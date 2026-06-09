{{! Example: ASR Direct Entity }}
**Example — Direct Entity (requirement explicitly names the entity type)**

Input:
- ASR: "The system shall cache authentication tokens to reduce database round-trips under high load."
  Quality attributes: [Performance Efficiency]

Expected output:
```json
{
  "proposed_name": "TokenCacheService",
  "c4_level": "container",
  "c4_type": "service",
  "description": "Caches authentication tokens in memory to reduce database round-trips during peak traffic.",
  "responsibilities": [
    "Store and invalidate authentication tokens",
    "Serve token validation requests from memory",
    "Evict expired tokens on a configurable TTL"
  ],
  "source_requirements": ["REQ-XXX"],
  "proposing_subgraph": "asr",
  "concern_technology": "Redis Cluster",
  "justification": "The requirement explicitly asks for token caching, which implies a dedicated cache service. Performance Efficiency weight justifies Redis as the technology choice for sub-millisecond lookups."
}
```
