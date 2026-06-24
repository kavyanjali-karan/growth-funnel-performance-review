SELECT

campaign_name,

SUM(signups) signups,

SUM(paid_users) paid,

SUM(revenue) revenue

FROM fact_growth_events

JOIN dim_campaign

USING(campaign_key)

GROUP BY campaign_name;