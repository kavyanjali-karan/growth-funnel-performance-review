/*
=====================================================
01_funnel_metrics.sql
Purpose:
Create executive funnel metrics and conversion rates
=====================================================
*/

WITH funnel_counts AS (

    SELECT
        COUNT(*) AS total_users,

        SUM(CASE WHEN stage_order >= 1 THEN 1 ELSE 0 END) AS visited_site,
        SUM(CASE WHEN stage_order >= 2 THEN 1 ELSE 0 END) AS signed_up,
        SUM(CASE WHEN stage_order >= 3 THEN 1 ELSE 0 END) AS completed_onboard,
        SUM(CASE WHEN stage_order >= 4 THEN 1 ELSE 0 END) AS activated_feature,
        SUM(CASE WHEN stage_order >= 5 THEN 1 ELSE 0 END) AS started_trial,
        SUM(CASE WHEN stage_order >= 6 THEN 1 ELSE 0 END) AS converted_paid

    FROM clean_funnel_data

),

funnel_metrics AS (

    SELECT
        visited_site,
        signed_up,
        completed_onboard,
        activated_feature,
        started_trial,
        converted_paid,

        ROUND(
            signed_up * 100.0 / NULLIF(visited_site,0),
            2
        ) AS visit_to_signup_pct,

        ROUND(
            completed_onboard * 100.0 / NULLIF(signed_up,0),
            2
        ) AS signup_to_onboard_pct,

        ROUND(
            activated_feature * 100.0 / NULLIF(completed_onboard,0),
            2
        ) AS onboard_to_activation_pct,

        ROUND(
            started_trial * 100.0 / NULLIF(activated_feature,0),
            2
        ) AS activation_to_trial_pct,

        ROUND(
            converted_paid * 100.0 / NULLIF(started_trial,0),
            2
        ) AS trial_to_paid_pct

    FROM funnel_counts

)

SELECT *
FROM funnel_metrics;