# User Acceptance Testing Plan

## Participants
Marketing Operations, Sales Operations, Data/IT, and product owner.

## Entry criteria
- Sample dataset available.
- Field mappings and validation rules reviewed.
- Pipeline executes successfully.
- Dashboard loads persisted records.

## UAT scenarios
| ID | Scenario | Expected result | Status |
|---|---|---|---|
| UAT-01 | Valid US lead with consent | Valid and assigned to a US queue | To execute |
| UAT-02 | Malformed email | Invalid, `invalid_email` reason shown | To execute |
| UAT-03 | Missing company | Invalid, routed to Data Quality Review | To execute |
| UAT-04 | Repeated email | Later occurrence sent to Duplicate Review | To execute |
| UAT-05 | Unknown consent status | Consent review error shown | To execute |
| UAT-06 | Unsupported country | Unsupported country error shown | To execute |
| UAT-07 | High score, GB region | EMEA - Priority | To execute |
| UAT-08 | Dashboard KPIs | Metrics match database query results | To execute |

## Exit criteria
- All critical scenarios pass.
- No unresolved severity-1 defects.
- Stakeholders approve the routing rules and exception ownership.
- Release notes and rollback approach are prepared for production integration.

## Release-readiness checklist
- [ ] Requirements signed off
- [ ] Field mappings approved
- [ ] Validation and consent rules reviewed
- [ ] UAT evidence recorded
- [ ] Monitoring and alert ownership assigned
- [ ] Support runbook and rollback plan approved
- [ ] User enablement communicated
