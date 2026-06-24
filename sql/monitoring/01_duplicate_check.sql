SELECT

customer_id,

COUNT(*)

FROM dim_customer

GROUP BY customer_id

HAVING COUNT(*)>1;