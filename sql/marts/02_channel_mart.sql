SELECT

channel_name,

SUM(visitors) visitors,

SUM(signups) signups,

SUM(revenue) revenue

FROM fact_growth_events

JOIN dim_channel

USING(channel_key)

GROUP BY channel_name;