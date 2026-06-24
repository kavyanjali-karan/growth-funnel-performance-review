SELECT

full_date,

SUM(visitors) visitors,

SUM(signups) signups,

SUM(trial_users) trials,

SUM(paid_users) paid,

SUM(revenue) revenue

FROM fact_growth_events

JOIN dim_date

USING(date_key)

GROUP BY full_date;