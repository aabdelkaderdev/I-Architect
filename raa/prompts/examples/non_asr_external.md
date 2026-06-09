{{! Example: Non-ASR External System }}
**Example — External System (functional requirement implies integration with an external system)**

Input:
- Non-ASR: "Users shall be able to log in using their Google account."

Expected output:
```json
{
  "proposed_name": "GoogleIdentityProviderSystem",
  "c4_level": "system",
  "c4_type": "external",
  "description": "External OAuth2 identity provider for Google account-based authentication.",
  "responsibilities": [
    "Authenticate users via Google OAuth2",
    "Provide identity claims to the application"
  ],
  "source_requirements": ["REQ-XXX"],
  "proposing_subgraph": "non_asr",
  "justification": "Google login requires integration with Google's OAuth2 identity provider, which is an external system outside the application boundary."
}
```
