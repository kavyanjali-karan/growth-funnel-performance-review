# Data Quality Validation Framework

The funnel dataset is validated before analysis.

## Validation Checks

1. Duplicate User IDs
2. Missing User IDs
3. Missing Signup Dates
4. Negative Revenue
5. Invalid Stage Order
6. Paid User Without Revenue
7. Revenue Without Paid Conversion
8. Future Signup Dates
9. Invalid Trial Flag

## Objective

Ensure analytical outputs are trustworthy before KPI reporting.

## Business Impact

Data quality failures can:

- Overstate conversion rates
- Inflate revenue projections
- Mislead stakeholder decisions

The validation layer is designed to mimic production BI workflows used in enterprise analytics teams.