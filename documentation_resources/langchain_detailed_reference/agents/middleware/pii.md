<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/pii -->

Modulev1.2.13 (latest)●Since v1.0

# pii

PII detection and handling middleware for agents.

## Attributes

[attribute

ResponseT](/python/langchain/agents/middleware/pii/ResponseT)

## Functions

[function

apply\_strategy

Apply the configured strategy to matches within content.](/python/langchain/agents/middleware/pii/apply_strategy)[function

detect\_credit\_card

Detect credit card numbers in content using Luhn validation.](/python/langchain/agents/middleware/pii/detect_credit_card)[function

detect\_email

Detect email addresses in content.](/python/langchain/agents/middleware/pii/detect_email)[function

detect\_ip

Detect IPv4 or IPv6 addresses in content.](/python/langchain/agents/middleware/pii/detect_ip)[function

detect\_mac\_address

Detect MAC addresses in content.](/python/langchain/agents/middleware/pii/detect_mac_address)[function

detect\_url

Detect URLs in content using regex and stdlib validation.](/python/langchain/agents/middleware/pii/detect_url)[function

hook\_config

Decorator to configure hook behavior in middleware methods.

Use this decorator on `before_model` or `after_model` methods in middleware classes
to configure their behavior. Currently supports specifying which destinations they
can jump to, which establishes conditional edges in the agent graph.](/python/langchain/agents/middleware/pii/hook_config)

## Classes

[class

PIIDetectionError

Raised when configured to block on detected sensitive values.](/python/langchain/agents/middleware/pii/PIIDetectionError)[class

PIIMatch

Represents an individual match of sensitive data.](/python/langchain/agents/middleware/pii/PIIMatch)[class

RedactionRule

Configuration for handling a single PII type.](/python/langchain/agents/middleware/pii/RedactionRule)[class

ResolvedRedactionRule

Resolved redaction rule ready for execution.](/python/langchain/agents/middleware/pii/ResolvedRedactionRule)[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/pii/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/pii/AgentState)[class

PIIMiddleware

Detect and handle Personally Identifiable Information (PII) in conversations.

This middleware detects common PII types and applies configurable strategies
to handle them. It can detect emails, credit cards, IP addresses, MAC addresses, and
URLs in both user input and agent output.

Built-in PII types:

- `email`: Email addresses
- `credit_card`: Credit card numbers (validated with Luhn algorithm)
- `ip`: IP addresses (validated with stdlib)
- `mac_address`: MAC addresses
- `url`: URLs (both `http`/`https` and bare URLs)

Strategies:

- `block`: Raise an exception when PII is detected
- `redact`: Replace PII with `[REDACTED_TYPE]` placeholders
- `mask`: Partially mask PII (e.g., `****-****-****-1234` for credit card)
- `hash`: Replace PII with deterministic hash (e.g., `<email_hash:a1b2c3d4>`)

Strategy Selection Guide:

| Strategy | Preserves Identity? | Best For |
| --- | --- | --- |
| `block` | N/A | Avoid PII completely |
| `redact` | No | General compliance, log sanitization |
| `mask` | No | Human readability, customer service UIs |
| `hash` | Yes (pseudonymous) | Analytics, debugging |](/python/langchain/agents/middleware/pii/PIIMiddleware)


