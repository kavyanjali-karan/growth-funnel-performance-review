SELECT

device_type,

SUM(visitors) visitors,

SUM(signups) signups

FROM fact_growth_events

JOIN dim_device

USING(device_key)

GROUP BY device_type;