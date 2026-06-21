# /*

dq_checks.sql
Business Intelligence Data Validation Framework
===============================================

*/

-- CHECK 1
-- Duplicate User IDs

SELECT
user_id,
COUNT(*) AS duplicate_count
FROM clean_funnel_data
GROUP BY user_id
HAVING COUNT(*) > 1;

---

-- CHECK 2
-- Missing User IDs

SELECT
COUNT(*) AS missing_user_ids
FROM clean_funnel_data
WHERE user_id IS NULL;

---

-- CHECK 3
-- Missing Signup Dates

SELECT
COUNT(*) AS missing_signup_dates
FROM clean_funnel_data
WHERE signup_date IS NULL;

---

-- CHECK 4
-- Invalid Revenue Values

SELECT
COUNT(*) AS invalid_revenue_records
FROM clean_funnel_data
WHERE monthly_revenue < 0;

---

-- CHECK 5
-- Invalid Funnel Stage

SELECT
COUNT(*) AS invalid_stage_records
FROM clean_funnel_data
WHERE stage_order NOT BETWEEN 1 AND 6;

---

-- CHECK 6
-- Paid Customer Without Revenue

SELECT
COUNT(*) AS paid_without_revenue
FROM clean_funnel_data
WHERE converted_paid = 1
AND monthly_revenue <= 0;

---

-- CHECK 7
-- Revenue Without Paid Conversion

SELECT
COUNT(*) AS revenue_without_paid_status
FROM clean_funnel_data
WHERE converted_paid = 0
AND monthly_revenue > 0;

---

-- CHECK 8
-- Future Signup Dates

SELECT
COUNT(*) AS future_signup_dates
FROM clean_funnel_data
WHERE signup_date > CURRENT_DATE;

---

-- CHECK 9
-- Trial Flag Consistency

SELECT
COUNT(*) AS invalid_trial_flags
FROM clean_funnel_data
WHERE reached_trial = 1
AND stage_order < 5;

---

-- CHECK 10
-- Country Distribution

SELECT
country,
COUNT(*) AS users
FROM clean_funnel_data
GROUP BY country
ORDER BY users DESC;
