SELECT

SUM(trial_users) trials,

SUM(paid_users) paid,

SUM(paid_users)/NULLIF(SUM(trial_users),0) paid_conversion

FROM growth_mart;