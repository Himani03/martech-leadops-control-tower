# Current State and Future State

## Current-state workflow
1. Campaign platform exports lead data.
2. Marketing Operations reviews spreadsheets manually.
3. Missing or invalid fields are corrected inconsistently.
4. Duplicate leads may reach sales queues.
5. Routing rules may vary by team or region.
6. Reporting is assembled after the fact, making root-cause analysis slow.

## Future-state workflow
1. Ingest records using a documented schema.
2. Normalize fields.
3. Validate required fields, email syntax, region, and consent status.
4. Detect duplicate normalized emails.
5. Enrich company attributes using an approved source (demo mapping in this project).
6. Score leads using transparent rules.
7. Route clean records to regional queues and exceptions to review queues.
8. Store the outcome and expose quality/routing KPIs.
9. Review recurring failure reasons and prioritize upstream fixes.

## Integration contract for a future connector
- Input: record ID, email, name, company, country, campaign/source, job title, consent status.
- Output: processing status, validation reasons, score, enrichment attributes, routing queue, processed timestamp.
- Failure behavior: log the failure, avoid silent drops, and place unresolved records into a retry or review queue.
