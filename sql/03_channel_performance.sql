/*
=====================================================
03_channel_analysis.sql
Purpose:
Measure acquisition channel effectiveness
=====================================================
*/

SELECT
    channel,

    COUNT(*) AS users,

    SUM(converted_paid) AS paid_users,

    SUM(monthly_revenue) AS monthly_revenue,

    ROUND(
        SUM(converted_paid) * 100.0 /
        NULLIF(COUNT(*),0),
        2
    ) AS paid_conversion_pct,

    ROUND(
        SUM(monthly_revenue) * 1.0 /
        NULLIF(COUNT(*),0),
        2
    ) AS revenue_per_user

FROM clean_funnel_data

GROUP BY channel

ORDER BY monthly_revenue DESC;