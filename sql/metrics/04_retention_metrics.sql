SELECT

SUM(active_customers) retained,

SUM(active_customers)/NULLIF(SUM(paid_users),0) retention_rate

FROM retention_mart;