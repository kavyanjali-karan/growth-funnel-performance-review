SELECT

SUM(visitors) visitors,

SUM(signups) signups,

SUM(signups)/NULLIF(SUM(visitors),0) signup_rate

FROM growth_mart;