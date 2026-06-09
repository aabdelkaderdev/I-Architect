{{! Example: ASR Indirect Entity }}
**Example — Indirect Entity (quality attribute implies an entity not named in requirements)**

Input:
- ASR: "The system shall handle 10,000 concurrent users with response times under 200ms."
  Quality attributes: [Performance Efficiency]

Expected output:
```json
{
  "proposed_name": "LoadBalancerService",
  "c4_level": "container",
  "c4_type": "service",
  "description": "Distributes incoming traffic across application server instances to meet concurrency and latency targets.",
  "responsibilities": [
    "Distribute requests across healthy backend instances",
    "Perform health checks on application servers",
    "Terminate TLS connections"
  ],
  "source_requirements": ["REQ-XXX"],
  "proposing_subgraph": "asr",
  "justification": "10,000 concurrent users with sub-200ms response requires horizontal scaling. A load balancer is the standard architectural pattern for distributing traffic across multiple instances — it is not named in the requirement but is implied by the performance target."
}
```
