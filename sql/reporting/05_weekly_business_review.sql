SELECT

full_date,

SUM(revenue),

SUM(signups),

SUM(paid_users)

FROM growth_mart

GROUP BY full_date;