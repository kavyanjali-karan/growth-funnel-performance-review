/*
=====================================================
06_dashboard_dataset.sql
Purpose:
Create dashboard-ready dataset for BI tools
=====================================================
*/

WITH funnel_base AS (

    SELECT

        user_id,
        signup_date,
        signup_month,
        signup_week,

        channel,
        device,
        country,
        plan,

        last_stage,
        stage_order,

        converted_paid,
        reached_trial,

        monthly_revenue

    FROM clean_funnel_data

),

segment_metrics AS (

    SELECT

        channel,
        device,
        country,
        plan,

        COUNT(*) AS users,

        SUM(converted_paid) AS paid_users,

        SUM(reached_trial) AS trial_users,

        SUM(monthly_revenue) AS revenue,

        ROUND(
            SUM(converted_paid) * 100.0 /
            NULLIF(COUNT(*),0),
            2
        ) AS paid_conversion_pct,

        ROUND(
            SUM(reached_trial) * 100.0 /
            NULLIF(COUNT(*),0),
            2
        ) AS trial_conversion_pct

    FROM funnel_base

    GROUP BY
        channel,
        device,
        country,
        plan

)

SELECT

    CURRENT_DATE AS refresh_date,

    channel,
    device,
    country,
    plan,

    users,
    trial_users,
    paid_users,

    revenue,

    paid_conversion_pct,
    trial_conversion_pct,

    ROUND(
        revenue /
        NULLIF(users,0),
        2
    ) AS revenue_per_user,

    ROUND(
        revenue /
        NULLIF(paid_users,0),
        2
    ) AS revenue_per_paid_user

FROM segment_metrics

ORDER BY revenue DESC;