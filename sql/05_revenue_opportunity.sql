/*
=====================================================
05_revenue_opportunity.sql
Purpose:
Estimate revenue recovery opportunities
=====================================================
*/

WITH device_performance AS (

    SELECT
        device,

        COUNT(*) AS users,

        SUM(converted_paid) AS paid_users,

        ROUND(
            SUM(converted_paid) * 1.0 /
            NULLIF(COUNT(*),0),
            4
        ) AS conversion_rate,

        AVG(monthly_revenue) AS avg_revenue

    FROM clean_funnel_data

    GROUP BY device

),

benchmark AS (

    SELECT
        MAX(conversion_rate) AS best_rate
    FROM device_performance

)

SELECT

    d.device,

    d.users,

    d.paid_users,

    ROUND(d.conversion_rate * 100,2)
        AS current_conversion_pct,

    ROUND(b.best_rate * 100,2)
        AS target_conversion_pct,

    ROUND(
        (b.best_rate - d.conversion_rate)
        * d.users,
        0
    ) AS additional_customers,

    ROUND(
        ((b.best_rate - d.conversion_rate)
        * d.users)
        * d.avg_revenue,
        2
    ) AS revenue_opportunity

FROM device_performance d
CROSS JOIN benchmark b

ORDER BY revenue_opportunity DESC;