SELECT

campaign_name,

SUM(revenue)

FROM campaign_mart

GROUP BY campaign_name;
