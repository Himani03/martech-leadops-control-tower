# Data Governance and Operations

## Data quality controls
- Required-field validation
- Email syntax checks
- Duplicate detection
- Country/region validation
- Consent-status review gate
- Explicit exception reason codes

## Operational ownership
- Marketing Operations: campaign field quality and source metadata.
- Sales Operations: routing queue definitions and handoff expectations.
- Data/IT: ingestion, mappings, persistence, logging, and incident response.
- Product owner: roadmap, requirements, prioritization, KPI review, and stakeholder sign-off.

## Suggested prioritization model
Prioritize issues using business impact, frequency, affected regions, compliance risk, and implementation effort. Consent/privacy issues and leads silently dropped from the funnel should receive urgent review.

## Production considerations
Use managed secrets, least-privilege access, encryption, retention rules, approved enrichment sources, audit logs, monitoring, retry policies, idempotent ingestion, and formal privacy/security review. This demo does not implement these production controls.
