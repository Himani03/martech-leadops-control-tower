# Product Requirements: MarTech LeadOps Control Tower

## Product vision
Improve marketing-to-sales lead handoff by making lead data more reliable, routing decisions transparent, and exceptions measurable.

## Users
- Marketing Operations: monitors lead intake quality and campaign source data.
- Sales Operations: needs reliable routing and clear ownership.
- Data/IT teams: investigate integration failures and maintain field mappings.
- Product owner: prioritizes enhancements and tracks outcomes.

## Problem statement
Lead records may contain invalid email addresses, missing company attributes, duplicate people, unsupported regions, or unclear consent status. Manual investigation slows handoff and reduces confidence in campaign reporting.

## Goals
1. Increase the share of records that pass required-field validation.
2. Make duplicate and consent-review exceptions visible.
3. Route valid records consistently using documented rules.
4. Provide operational KPIs for review and prioritization.
5. Establish requirements and UAT artifacts suitable for a cross-functional release.

## Out of scope
- Real Marketo, Salesforce, Adobe Experience Platform, or ServiceNow integration.
- Production-grade identity resolution or third-party enrichment.
- Automated legal decisions about consent.
- Predictive scoring trained on real conversion outcomes.

## Functional requirements
- FR-01: Ingest lead records from a documented CSV schema.
- FR-02: Normalize email and country values before validation.
- FR-03: Validate email syntax, first/last name, company, supported country, and consent status.
- FR-04: Flag repeated normalized emails for duplicate review.
- FR-05: Enrich company industry and size using a clearly labeled demo mapping.
- FR-06: Calculate a transparent 0-100 rule-based score.
- FR-07: Route invalid and duplicate records to separate review queues.
- FR-08: Route valid records to a region and priority queue.
- FR-09: Persist processed records and validation reasons in SQLite.
- FR-10: Display quality, volume, and routing KPIs in a dashboard.

## User stories and acceptance criteria
**US-01: As Marketing Operations, I want to see invalid records and reasons so that I can correct upstream campaign data.**
- Given a lead with an invalid email, when processing runs, then the record is marked invalid and includes `invalid_email`.
- Given a lead with a missing company, when processing runs, then the record is sent to Data Quality Review.

**US-02: As Sales Operations, I want duplicate emails flagged so that duplicate records are not routed as new leads.**
- Given two records with the same normalized email, when processing runs, then the later record is flagged as duplicate and sent to Duplicate Review.

**US-03: As a sales operations user, I want consistent regional routing.**
- Given a valid US lead, when the score is 70 or higher, then it is assigned to North America - Priority.
- Given a valid GB lead below 70, when processing runs, then it is assigned to EMEA - Standard.

**US-04: As a product owner, I want operational KPIs so that I can measure the quality of the lead handoff.**
- Given processed records, when the dashboard opens, then it displays volume, valid rate, invalid count, duplicate count, and routed count from persisted data.

## Non-functional requirements
- Keep validation and routing rules readable and testable.
- Do not store credentials in source control.
- Use synthetic data only.
- Preserve exception reasons for auditability.
- Dashboard should remain usable for a small portfolio dataset.

## Success metrics
- Valid-record rate = valid records / total records.
- Duplicate rate = duplicate records / total records.
- Routing coverage = valid, nonduplicate records assigned to a regional queue / valid, nonduplicate records.
- Exception resolution time = time from exception creation to correction (future integration metric).
- UAT pass rate = passed scenarios / executed scenarios.

## Dependencies and risks
- Field mapping depends on upstream CRM/marketing automation schema.
- Real enrichment requires approved provider and usage terms.
- Consent and privacy logic must be reviewed by qualified compliance stakeholders.
- Production deployment requires authentication, role-based access, observability, retries, and integration monitoring.
