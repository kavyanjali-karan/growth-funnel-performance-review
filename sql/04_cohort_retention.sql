/*
=====================================================
04_cohort_retention.sql
Purpose:
Create monthly cohort analysis
=====================================================
*/

WITH cohorts AS (

    SELECT
        signup_month,

        COUNT(*) AS users,

        SUM(reached_trial) AS trial_users,

        SUM(converted_paid) AS paid_users

    FROM clean_funnel_data

    GROUP BY signup_month

)

SELECT

    signup_month,

    users,

    trial_users,

    paid_users,

    ROUND(
        trial_users * 100.0 /
        NULLIF(users,0),
        2
    ) AS trial_rate_pct,

    ROUND(
        paid_users * 100.0 /
        NULLIF(users,0),
        2
    ) AS paid_rate_pct

FROM cohorts

ORDER BY signup_month;