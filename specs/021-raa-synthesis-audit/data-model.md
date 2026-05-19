# Data Model: RAA Audit Checklist

Since this is an audit task, the data model consists of the verification metrics.

- **Entity**: `Audit Item`
  - `id`: string
  - `description`: string
  - `status`: Pass | Fail | Incomplete
  - `findings`: string
