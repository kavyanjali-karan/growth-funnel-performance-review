/*
=====================================================
02_device_analysis.sql
Purpose:
Evaluate funnel performance by device
=====================================================
*/

WITH device_summary AS (

    SELECT
        device,

        COUNT(*) AS users,

        SUM(converted_paid) AS paid_users,

        SUM(monthly_revenue) AS monthly_revenue,

        ROUND(
            SUM(converted_paid) * 100.0 /
            NULLIF(COUNT(*),0),
            2
        ) AS paid_conversion_pct

    FROM clean_funnel_data
    GROUP BY device

),

best_device AS (

    SELECT
        MAX(paid_conversion_pct) AS benchmark_rate
    FROM device_summary

)

SELECT
    d.device,
    d.users,
    d.paid_users,
    d.monthly_revenue,
    d.paid_conversion_pct,

    ROUND(
        (b.benchmark_rate - d.paid_conversion_pct),
        2
    ) AS conversion_gap_pct

FROM device_summary d
CROSS JOIN best_device b
ORDER BY paid_conversion_pct DESC;