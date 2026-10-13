# MarTech LeadOps Control Tower

A portfolio project demonstrating how a Data Product Manager can improve B2B marketing lead operations through data quality controls, lead enrichment, scoring, routing, integrations, and measurable operational outcomes.

> Portfolio/demo project using synthetic data. It is not affiliated with or endorsed by ServiceNow. It does not connect to real CRM or marketing automation systems.

## Business problem
Marketing teams lose time and pipeline when lead records arrive incomplete, duplicated, invalid, or without a clear owner. This project models an end-to-end lead operations workflow and makes the process measurable.

## What it does
- Ingests synthetic campaign leads from CSV.
- Normalizes fields and validates email, company, country, consent, and required attributes.
- Detects duplicates and flags records for review rather than silently discarding them.
- Enriches records with demo firmographic values using a transparent, deterministic ruleset.
- Calculates a configurable lead score and assigns a sales region/queue.
- Stores lead records and processing outcomes in SQLite.
- Exposes summary KPIs and a Streamlit operations dashboard.
- Includes SQL analysis, acceptance criteria, UAT scenarios, and automated tests.

## Architecture
```text
Synthetic CSV / future CRM or Marketo connector
                 |
                 v
        Ingestion + normalization
                 |
                 v
      Validation + duplicate detection
                 |
                 v
     Demo enrichment + lead scoring
                 |
                 v
         Routing / exception queue
                 |
          +------+------+
          |             |
          v             v
      SQLite DB     Streamlit KPI dashboard
          |
          v
    SQL reporting / audit trail
```

## Run locally
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m app.pipeline
streamlit run app/dashboard.py
```

The pipeline creates `data/leadops.db` and processes `data/sample_leads.csv`. The dashboard reads the database.

## Project layout
- `app/pipeline.py`: ingestion, validation, deduplication, enrichment, scoring, routing, persistence.
- `app/dashboard.py`: KPI dashboard.
- `app/db.py`: database schema and persistence helpers.
- `data/sample_leads.csv`: synthetic sample input.
- `sql/leadops_analysis.sql`: example operational reporting queries.
- `docs/`: product requirements, workflow, UAT, and KPI definitions.
- `tests/`: unit tests for key data rules.
- `requirements.txt`: Python dependencies.

## Example KPIs
The dashboard reports total leads, valid leads, invalid records, duplicate records, routed leads, average lead score, and routing distribution. Metrics are calculated from the run data rather than hard-coded.

## Product management artifacts
This repository intentionally includes product documentation, not only code:
- Problem statement and scope
- Current-state and future-state workflows
- Functional requirements and user stories
- Acceptance criteria and success metrics
- UAT plan and release-readiness checklist
- Governance and exception-handling decisions

## Important assumptions
This is a learning/portfolio implementation. Enrichment values and routing rules are illustrative, not real third-party data. Consent handling is modeled as a validation gate; this is not legal advice or a production compliance implementation. Production use would require approved integrations, security review, access controls, monitoring, and privacy review.

## Suggested resume wording
After running and reviewing the project, you can describe it as a portfolio project:

**MarTech LeadOps Control Tower | Python, SQL, SQLite, Streamlit, Data Quality, Product Requirements**
- Built a lead operations prototype that validates, deduplicates, enriches, scores, and routes synthetic B2B marketing leads through a documented workflow.
- Defined product requirements, user stories, acceptance criteria, UAT scenarios, and KPIs for lead quality, routing coverage, and exception handling.
- Created SQL reporting and a dashboard to monitor lead funnel health, data-quality failures, duplicates, and routing outcomes.

Only include measured numerical impact after you run experiments and calculate it from the generated data. Do not claim production deployment or direct experience with Marketo/Adobe unless you have it.
