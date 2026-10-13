from app.pipeline import validate_lead, score_lead, route_lead

def valid_row():
    return {
        "email": "test@example.com", "first_name": "Test", "last_name": "User",
        "company": "CloudNorth", "country": "US", "job_title": "IT Director",
        "source_campaign": "Product Demo Webinar", "consent_status": "opted_in"
    }

def test_valid_record_has_no_errors():
    assert validate_lead(valid_row()) == []

def test_invalid_email_is_flagged():
    row = valid_row()
    row["email"] = "not-an-email"
    assert "invalid_email" in validate_lead(row)

def test_missing_company_is_flagged():
    row = valid_row()
    row["company"] = ""
    assert "missing_company" in validate_lead(row)

def test_consent_review_is_required_for_unknown_status():
    row = valid_row()
    row["consent_status"] = "unknown"
    assert "consent_review_required" in validate_lead(row)

def test_high_intent_record_scores_at_least_70():
    assert score_lead(valid_row()) >= 70

def test_duplicate_goes_to_review_queue():
    row = valid_row()
    assert route_lead(row, 90, True, True) == "Duplicate Review"

def test_invalid_record_goes_to_data_quality_queue():
    assert route_lead(valid_row(), 90, False, False) == "Data Quality Review"
