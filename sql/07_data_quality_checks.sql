/*
=====================================================
07_data_quality_checks.sql
Purpose:
Validate quality of funnel dataset
=====================================================
*/

-----------------------------------------------------
-- CHECK 1
-- Duplicate User IDs
-----------------------------------------------------

SELECT
    'duplicate_user_ids' AS check_name,
    COUNT(*) AS issue_count
FROM (

    SELECT
        user_id
    FROM clean_funnel_data
    GROUP BY user_id
    HAVING COUNT(*) > 1

) duplicates;

-----------------------------------------------------
-- CHECK 2
-- Missing User IDs
-----------------------------------------------------

SELECT
    'missing_user_ids' AS check_name,
    COUNT(*) AS issue_count
FROM clean_funnel_data
WHERE user_id IS NULL;

-----------------------------------------------------
-- CHECK 3
-- Missing Signup Date
-----------------------------------------------------

SELECT
    'missing_signup_date' AS check_name,
    COUNT(*) AS issue_count
FROM clean_funnel_data
WHERE signup_date IS NULL;

-----------------------------------------------------
-- CHECK 4
-- Invalid Revenue
-----------------------------------------------------

SELECT
    'negative_revenue' AS check_name,
    COUNT(*) AS issue_count
FROM clean_funnel_data
WHERE monthly_revenue < 0;

-----------------------------------------------------
-- CHECK 5
-- Invalid Stage Order
-----------------------------------------------------

SELECT
    'invalid_stage_order' AS check_name,
    COUNT(*) AS issue_count
FROM clean_funnel_data
WHERE stage_order NOT BETWEEN 1 AND 6;

-----------------------------------------------------
-- CHECK 6
-- Paid User Without Revenue
-----------------------------------------------------

SELECT
    'paid_user_without_revenue' AS check_name,
    COUNT(*) AS issue_count
FROM clean_funnel_data
WHERE converted_paid = 1
AND monthly_revenue <= 0;

-----------------------------------------------------
-- CHECK 7
-- Revenue Without Paid Conversion
-----------------------------------------------------

SELECT
    'revenue_without_paid_status' AS check_name,
    COUNT(*) AS issue_count
FROM clean_funnel_data
WHERE monthly_revenue > 0
AND converted_paid = 0;

-----------------------------------------------------
-- CHECK 8
-- Future Signup Dates
-----------------------------------------------------

SELECT
    'future_signup_date' AS check_name,
    COUNT(*) AS issue_count
FROM clean_funnel_data
WHERE signup_date > CURRENT_DATE;

-----------------------------------------------------
-- CHECK 9
-- Trial Flag Validation
-----------------------------------------------------

SELECT
    'invalid_trial_flag' AS check_name,
    COUNT(*) AS issue_count
FROM clean_funnel_data
WHERE reached_trial = 1
AND stage_order < 5;

-----------------------------------------------------
-- CHECK 10
-- Country Coverage
-----------------------------------------------------

SELECT
    country,
    COUNT(*) AS users
FROM clean_funnel_data
GROUP BY country
ORDER BY users DESC;