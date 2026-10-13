-- Run these queries against data/leadops.db using SQLite.

-- 1. Overall data quality and routing summary
SELECT
  COUNT(*) AS total_leads,
  SUM(is_valid) AS valid_leads,
  SUM(CASE WHEN is_valid = 0 THEN 1 ELSE 0 END) AS invalid_leads,
  SUM(is_duplicate) AS duplicate_leads,
  SUM(CASE WHEN processing_status = 'routed' THEN 1 ELSE 0 END) AS routed_leads,
  ROUND(100.0 * SUM(is_valid) / NULLIF(COUNT(*), 0), 1) AS valid_rate_pct
FROM lead_processing;

-- 2. Most common validation issues
SELECT validation_errors, COUNT(*) AS records
FROM lead_processing
WHERE is_valid = 0
GROUP BY validation_errors
ORDER BY records DESC;

-- 3. Queue distribution
SELECT route_queue, COUNT(*) AS lead_count,
       ROUND(AVG(lead_score), 1) AS average_score
FROM lead_processing
GROUP BY route_queue
ORDER BY lead_count DESC;

-- 4. Campaign-level quality
SELECT source_campaign, COUNT(*) AS total,
       SUM(is_valid) AS valid,
       SUM(is_duplicate) AS duplicates
FROM lead_processing
GROUP BY source_campaign
ORDER BY total DESC;
