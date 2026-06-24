SELECT

segment,

COUNT(DISTINCT customer_id) customers,

SUM(revenue) revenue

FROM fact_growth_events

JOIN dim_customer

USING(customer_key)

GROUP BY segment;