SELECT

channel_name,

SUM(revenue)

FROM channel_mart

GROUP BY channel_name;