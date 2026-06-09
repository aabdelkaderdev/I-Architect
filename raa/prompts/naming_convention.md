{{! Naming Convention — included in all system prompts }}
Entity naming rules (MUST be followed exactly):

1. Names are PascalCase: no spaces, hyphens, or underscores. Start each word with
   a capital letter.
2. Every entity name MUST end with a type suffix matching its c4_type:

   | c4_type   | Required suffix | Example                  |
   |-----------|-----------------|--------------------------|
   | service   | Service         | AuthenticationService    |
   | database  | Database        | UserDatabase             |
   | gateway   | Gateway         | ApiGateway               |
   | queue     | Queue           | NotificationQueue        |
   | store     | Store           | SessionStore             |
   | external  | System          | PaymentGatewaySystem     |
   | actor     | (no suffix)     | EndUser, SystemAdmin     |

3. Actors carry no suffix — the name stands alone.
4. Use the most generic canonical term. Do not use synonyms.
   Good: AuthenticationService. Bad: AuthService, LoginService.
