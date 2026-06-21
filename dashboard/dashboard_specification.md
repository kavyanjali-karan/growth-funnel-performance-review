# Dashboard Specification

## Dashboard Name

SaaS Funnel Performance Dashboard

---

# Purpose

Provide executive visibility into customer acquisition, funnel performance, revenue generation, and conversion optimization opportunities.

The dashboard is designed for:

* Executive Leadership
* Revenue Teams
* Product Teams
* Marketing Teams
* Business Intelligence Teams

---

# Dashboard Objectives

1. Monitor funnel health.
2. Identify conversion bottlenecks.
3. Compare segment performance.
4. Track recurring revenue.
5. Prioritize optimization opportunities.
6. Support strategic decision-making.

---

# Data Source

Primary Dataset:

dashboard_dataset

Generated From:

sql/06_dashboard_dataset.sql

Refresh Frequency:

Daily

---

# Page 1: Executive Overview

## KPI Cards

Total Users

Formula:

COUNT(users)

---

Paid Customers

Formula:

SUM(paid_users)

---

Paid Conversion Rate

Formula:

Paid Customers / Users

---

Monthly Recurring Revenue

Formula:

SUM(revenue)

---

Revenue Per User

Formula:

Revenue / Users

---

## Visuals

### Funnel Conversion

Type:

Funnel Chart

Metrics:

* Visitors
* Signups
* Onboarding
* Activation
* Trial
* Paid

Purpose:

Identify funnel leakage.

---

### Revenue Breakdown

Type:

Bar Chart

Dimension:

Channel

Metric:

Revenue

Purpose:

Identify highest revenue sources.

---

### Device Performance

Type:

Bar Chart

Dimension:

Device

Metric:

Paid Conversion Rate

Purpose:

Compare conversion efficiency.

---

# Page 2: Acquisition Analysis

## Visuals

### Channel Performance

Dimensions:

* Channel

Metrics:

* Users
* Paid Users
* Revenue
* Revenue Per User

Purpose:

Evaluate acquisition quality.

---

### Country Performance

Dimensions:

* Country

Metrics:

* Revenue
* Paid Conversion Rate

Purpose:

Evaluate geographic opportunities.

---

### Plan Distribution

Dimensions:

* Plan

Metrics:

* Revenue
* Paid Users

Purpose:

Understand subscription mix.

---

# Page 3: Conversion Analysis

## Visuals

### Device Funnel

Dimension:

Device

Metrics:

* Trial Rate
* Paid Rate

Purpose:

Identify friction points.

---

### Conversion Heatmap

Dimensions:

* Device
* Channel

Metric:

Paid Conversion Rate

Purpose:

Detect underperforming combinations.

---

### Segment Ranking

Dimensions:

* Device
* Channel

Metrics:

* Revenue Opportunity

Purpose:

Prioritize optimization initiatives.

---

# Page 4: Revenue Opportunity

## Visuals

### Revenue Recovery

Dimension:

Device

Metric:

Revenue Opportunity

Purpose:

Estimate incremental revenue.

---

### Opportunity Prioritization Matrix

Axes:

X = Effort

Y = Impact

Purpose:

Guide investment decisions.

---

# Filters

Global Filters:

* Signup Month
* Device
* Channel
* Country
* Plan

---

# Success Criteria

The dashboard should allow stakeholders to answer:

* Where are customers dropping off?
* Which segments underperform?
* How much revenue is at risk?
* What should be optimized first?
* Which initiatives create the highest ROI?
