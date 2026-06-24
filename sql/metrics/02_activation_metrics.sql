SELECT

SUM(activated_users) activated,

SUM(activated_users)/NULLIF(SUM(signups),0) activation_rate

FROM growth_mart;