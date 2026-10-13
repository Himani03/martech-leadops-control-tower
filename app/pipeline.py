from pathlib import Path
import csv
import json
import re
from datetime import datetime, timezone
import pandas as pd
from app.db import initialize_db, connect, DB_PATH

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "sample_leads.csv"

EMAIL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")
VALID_COUNTRIES = {"US", "CA", "GB", "DE", "IN", "AU"}
INDUSTRY_MAP = {
    "cloudnorth": "Technology", "brightpath": "Professional Services",
    "greenfield": "Manufacturing", "summitcare": "Healthcare",
    "bluepeak": "Financial Services", "orbitworks": "Technology"
}

def normalize(value):
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()

def validate_lead(row):
    errors = []
    email = normalize(row.get("email")).lower()
    company = normalize(row.get("company"))
    country = normalize(row.get("country")).upper()
    consent = normalize(row.get("consent_status")).lower()
    if not email or not EMAIL_RE.match(email):
        errors.append("invalid_email")
    if not normalize(row.get("first_name")):
        errors.append("missing_first_name")
    if not normalize(row.get("last_name")):
        errors.append("missing_last_name")
    if not company:
        errors.append("missing_company")
    if country not in VALID_COUNTRIES:
        errors.append("unsupported_or_missing_country")
    if consent not in {"opted_in", "legitimate_interest"}:
        errors.append("consent_review_required")
    return errors

def enrich_company(company):
    company_clean = normalize(company).lower()
    for key, industry in INDUSTRY_MAP.items():
        if key in company_clean.replace(" ", ""):
            return industry, "201-1000" if industry == "Technology" else "51-200"
    return "Unknown", "Unknown"

def score_lead(row):
    score = 0
    email = normalize(row.get("email")).lower()
    company = normalize(row.get("company"))
    campaign = normalize(row.get("source_campaign")).lower()
    consent = normalize(row.get("consent_status")).lower()
    if EMAIL_RE.match(email):
        score += 25
    if company:
        score += 20
    if normalize(row.get("job_title")):
        score += 15
    if any(word in campaign for word in ("demo", "webinar", "product")):
        score += 20
    if consent in {"opted_in", "legitimate_interest"}:
        score += 20
    return min(score, 100)

def route_lead(row, score, valid, duplicate):
    if duplicate:
        return "Duplicate Review"
    if not valid:
        return "Data Quality Review"
    country = normalize(row.get("country")).upper()
    if score >= 70:
        return {"US": "North America - Priority", "CA": "North America - Priority",
                "GB": "EMEA - Priority", "DE": "EMEA - Priority",
                "IN": "APAC - Priority", "AU": "APAC - Priority"}.get(country, "General Queue")
    return {"US": "North America - Standard", "CA": "North America - Standard",
            "GB": "EMEA - Standard", "DE": "EMEA - Standard",
            "IN": "APAC - Standard", "AU": "APAC - Standard"}.get(country, "General Queue")

def process_file(input_path=INPUT_PATH, db_path=DB_PATH):
    initialize_db(db_path)
    df = pd.read_csv(input_path, dtype=str).fillna("")
    seen_emails = set()
    records = []
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for _, raw in df.iterrows():
        row = {k: normalize(v) for k, v in raw.to_dict().items()}
        email = row.get("email", "").lower()
        errors = validate_lead(row)
        duplicate = bool(email and email in seen_emails)
        if email:
            seen_emails.add(email)
        industry, company_size = enrich_company(row.get("company"))
        score = score_lead(row)
        valid = len(errors) == 0
        queue = route_lead(row, score, valid, duplicate)
        status = "duplicate_review" if duplicate else ("invalid_review" if not valid else "routed")
        records.append({
            "record_id": row.get("record_id") or f"ROW-{len(records)+1:04d}",
            "email": row.get("email", ""), "first_name": row.get("first_name", ""),
            "last_name": row.get("last_name", ""), "company": row.get("company", ""),
            "country": row.get("country", "").upper(),
            "source_campaign": row.get("source_campaign", ""),
            "consent_status": row.get("consent_status", ""),
            "normalized_email": email, "is_valid": int(valid),
            "validation_errors": json.dumps(errors), "is_duplicate": int(duplicate),
            "industry": industry, "company_size": company_size, "lead_score": score,
            "route_queue": queue, "processing_status": status, "processed_at": now
        })
    with connect(db_path) as conn:
        conn.execute("DELETE FROM lead_processing")
        conn.executemany("""
            INSERT OR REPLACE INTO lead_processing
            (record_id,email,first_name,last_name,company,country,source_campaign,
             consent_status,normalized_email,is_valid,validation_errors,is_duplicate,
             industry,company_size,lead_score,route_queue,processing_status,processed_at)
            VALUES (:record_id,:email,:first_name,:last_name,:company,:country,:source_campaign,
             :consent_status,:normalized_email,:is_valid,:validation_errors,:is_duplicate,
             :industry,:company_size,:lead_score,:route_queue,:processing_status,:processed_at)
        """, records)
    print(f"Processed {len(records)} records into {db_path}")
    print(f"Valid: {sum(r['is_valid'] for r in records)} | Duplicates: {sum(r['is_duplicate'] for r in records)}")
    return records

if __name__ == "__main__":
    process_file()
