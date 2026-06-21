# Star Schema Design

## Objective

Design a dimensional data model capable of supporting executive reporting, dashboarding, KPI monitoring, and ad hoc business intelligence analysis.

---

# Business Process

The business process being modeled is:

Customer Funnel Progression

Users progress through stages:

1. Visit Site
2. Sign Up
3. Complete Onboarding
4. Activate Feature
5. Start Trial
6. Convert to Paid

---

# Grain

One record per user.

Each record represents the most recent known funnel state of a customer.

---

# Fact Table

fact_funnel_events

Measures:

* monthly_revenue
* converted_paid
* reached_trial
* stage_order

Foreign Keys:

* customer_key
* date_key
* device_key
* channel_key

---

# Dimension Tables

## dim_customer

Customer attributes.

Columns:

* customer_key
* user_id
* country
* plan

---

## dim_date

Calendar dimension.

Columns:

* date_key
* full_date
* year
* quarter
* month
* week
* day

---

## dim_device

Device dimension.

Columns:

* device_key
* device

Values:

* Desktop
* Mobile
* Tablet

---

## dim_channel

Acquisition source dimension.

Columns:

* channel_key
* channel

Examples:

* Organic Search
* Paid Search
* Referral
* Social
* Direct

---

# Logical Schema

```
             dim_customer
                   |
                   |
                   |
```

dim_date ----- fact_funnel_events ----- dim_device
|
|
|
dim_channel

---

# Example Business Questions Supported

### Funnel Performance

* What percentage of users become paid customers?

### Device Analysis

* Which device converts best?

### Channel Analysis

* Which acquisition source drives the most revenue?

### Revenue Analysis

* What is monthly recurring revenue by segment?

### Cohort Analysis

* How do signup cohorts perform over time?

---

# Benefits

This dimensional model enables:

* Executive reporting
* Dashboard development
* KPI monitoring
* Cohort analysis
* Funnel analysis
* Revenue analysis
* Self-service business intelligence

The design follows common Business Intelligence practices used in Snowflake, Redshift, BigQuery, SQL Server, and modern cloud data warehouses.
