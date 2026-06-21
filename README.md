# SaaS Conversion Funnel Intelligence | Business Intelligence Case Study

## Executive Summary

This project analyzes a SaaS customer acquisition funnel to identify conversion bottlenecks, quantify revenue leakage, and prioritize business actions that improve recurring revenue.

Using funnel analytics, segmentation analysis, revenue modeling, SQL reporting, dimensional modeling, and executive reporting techniques, the project identified an estimated **$8,828/month recoverable revenue opportunity** driven primarily by mobile onboarding friction.

The project was designed to simulate a Business Intelligence workflow, covering data generation, data quality validation, KPI development, SQL analysis, stakeholder reporting, dashboard planning, and executive recommendations.

---

# Business Problem

A SaaS company had visibility into overall revenue but lacked a structured framework to understand:

* Where users were dropping out of the acquisition funnel
* Which customer segments were underperforming
* What revenue impact those inefficiencies created
* Which initiatives should be prioritized

Without funnel-level visibility, optimization efforts were largely based on assumptions rather than measurable evidence.

---

# Business Objectives

The analysis was designed to:

* Measure end-to-end funnel performance
* Identify conversion bottlenecks
* Evaluate acquisition channel effectiveness
* Compare device-level performance
* Quantify recoverable revenue opportunities
* Design KPI reporting frameworks
* Support executive decision-making

---

# Key Results

| Metric                   | Value        |
| ------------------------ | ------------ |
| Total Users              | 9,995        |
| Paid Customers           | 277          |
| Funnel Conversion Rate   | 2.8%         |
| Monthly Revenue          | $19,563      |
| Revenue Opportunity      | $8,828/month |
| Referral Conversion Rate | 7.8%         |
| Social Conversion Rate   | 0.2%         |

---

# Funnel Performance

| Stage                | Users | Step Conversion | Overall Conversion |
| -------------------- | ----- | --------------- | ------------------ |
| Visited Site         | 9,995 | 100.0%          | 100.0%             |
| Signed Up            | 3,632 | 36.3%           | 36.3%              |
| Completed Onboarding | 1,984 | 54.6%           | 19.8%              |
| Activated Feature    | 1,255 | 63.3%           | 12.6%              |
| Started Trial        | 695   | 55.4%           | 7.0%               |
| Converted To Paid    | 277   | 39.9%           | 2.8%               |

---

# Visual Analysis

## Funnel Overview

![Funnel Overview](charts/01_funnel_overview.png)

## Step Conversion Analysis

![Step Conversion](charts/02_step_conversion.png)

## Device Conversion Analysis

![Device Conversion](charts/03_device_conversion.png)

## Channel Conversion Analysis

![Channel Conversion](charts/04_channel_conversion.png)

## Monthly Performance Trend

![Monthly Trend](charts/05_monthly_trend.png)

## Revenue Opportunity Analysis

![Revenue Opportunity](charts/06_revenue_opportunity.png)

---

# Key Findings

## Mobile Conversion Gap

Mobile users convert significantly worse than desktop users.

Business Impact:

A major portion of potential recurring revenue is lost during mobile onboarding.

Estimated Opportunity:

$8,828 monthly recurring revenue.

Recommendation:

Redesign the mobile onboarding flow to reduce friction and improve activation.

---

## Trial-To-Paid Bottleneck

The largest monetization loss occurs after trial adoption.

Business Impact:

Customer acquisition investment is not converting efficiently into paying customers.

Recommendation:

Improve upgrade messaging, product education, and pricing communication.

---

## Acquisition Channel Quality Differences

Referral traffic significantly outperforms social-media traffic.

Business Impact:

Marketing spend allocation is suboptimal.

Recommendation:

Increase investment in referral acquisition programs and reduce low-performing social spending.

---

# Business Intelligence Deliverables

## SQL Analytics Layer

The project includes warehouse-style SQL analyses for KPI reporting and business monitoring.

* Funnel Metrics Reporting
* Device Performance Analysis
* Channel Performance Analysis
* Cohort Retention Analysis
* Revenue Opportunity Modeling
* Dashboard Dataset Creation
* Data Quality Validation

---

## Executive Reporting

Business deliverables include:

* Executive Summary
* Business Case
* Stakeholder Recommendations
* KPI Dictionary
* Experimentation Plan

---

## Data Modeling

A dimensional model was designed to support analytical reporting.

Includes:

* Fact Table Design
* Dimension Table Design
* Star Schema Documentation
* Dashboard Data Structures

---

## Data Quality Framework

Validation checks ensure KPI reliability before reporting.

Checks include:

* Duplicate Detection
* Missing Values
* Revenue Consistency
* Funnel Stage Validation
* Trial Conversion Validation
* Date Validation

---

# Technical Skills Demonstrated

## Analytics

* Funnel Analysis
* Conversion Analysis
* Cohort Analysis
* Revenue Opportunity Analysis
* KPI Design

## SQL

* Common Table Expressions (CTEs)
* Aggregations
* Segmentation Analysis
* Cohort Reporting
* Dashboard Data Marts
* Data Quality Validation

## Python

* Data Generation
* Data Cleaning
* Data Validation
* Exploratory Analysis
* Revenue Modeling
* Data Visualization

## Business Intelligence

* Executive Reporting
* KPI Governance
* Dashboard Planning
* Stakeholder Communication
* Experimentation Planning
* Revenue Prioritization

## Data Modeling

* Star Schema Design
* Fact Tables
* Dimension Tables
* Analytical Warehousing Concepts

---

# Recommendations

## Priority 1

Mobile Onboarding Optimization

Expected Impact:

Very High

---

## Priority 2

Trial-To-Paid Conversion Improvement

Expected Impact:

Very High

---

## Priority 3

Referral Program Expansion

Expected Impact:

High

---

# Project Structure

```
saas-funnel-analysis/

│   .gitignore
│   README.md
│   requirements.txt
│
├── charts
│   ├── 01_funnel_overview.png
│   ├── 02_step_conversion.png
│   ├── 03_device_conversion.png
│   ├── 04_channel_conversion.png
│   ├── 05_monthly_trend.png
│   └── 06_revenue_opportunity.png
│
├── dashboard
│   ├── dashboard_specification.md
│   ├── dashboard_wireframe.md
│   └── stakeholder_views.md
│
├── data
│   ├── raw_funnel_data.csv
│   ├── clean_funnel_data.csv
│   ├── funnel_summary.csv
│   ├── device_funnel.csv
│   ├── channel_funnel.csv
│   ├── monthly_trend.csv
│   └── revenue_opportunity.csv
│
├── data_quality
│   ├── dq_checks.sql
│   ├── dq_report.csv
│   └── validation_framework.md
│
├── docs
│   ├── business_case.md
│   ├── executive_summary.md
│   ├── experimentation_plan.md
│   ├── metric_dictionary.md
│   └── stakeholder_recommendations.md
│
├── modeling
│   ├── fact_funnel_events.sql
│   ├── dim_customer.sql
│   ├── dim_date.sql
│   ├── dim_device.sql
│   ├── dim_channel.sql
│   └── star_schema.md
│
├── notebooks
│   ├── phase1_setup.py
│   ├── phase2_generate_data.py
│   ├── phase3_clean_data.py
│   ├── phase4_analyze.py
│   ├── phase5_visualize.py
│   └── phase6_package.py
│
├── outputs
│   ├── executive_report.md
│   └── management_summary.md
│
└── sql
    ├── 01_funnel_metrics.sql
    ├── 02_device_performance.sql
    ├── 03_channel_performance.sql
    ├── 04_cohort_retention.sql
    ├── 05_revenue_opportunity.sql
    ├── 06_dashboard_dataset.sql
    └── 07_data_quality_checks.sql
```

---

# How To Run

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/saas-funnel-analysis.git
cd saas-funnel-analysis
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Pipeline

```bash
python notebooks/phase1_setup.py

python notebooks/phase2_generate_data.py

python notebooks/phase3_clean_data.py

python notebooks/phase4_analyze.py

python notebooks/phase5_visualize.py

python notebooks/phase6_package.py
```

---

# Expected Outputs

Running the project will generate:

### Processed Data

* clean_funnel_data.csv
* funnel_summary.csv
* device_funnel.csv
* channel_funnel.csv
* monthly_trend.csv
* revenue_opportunity.csv

### Visualizations

* Funnel Overview
* Step Conversion Analysis
* Device Conversion Analysis
* Channel Conversion Analysis
* Monthly Trend Analysis
* Revenue Opportunity Analysis

### Business Deliverables

* Executive Report
* Management Summary
* Stakeholder Recommendations
* KPI Documentation

---

# Executive Conclusion

The largest growth opportunity is not increasing acquisition volume.

The highest-value opportunity is improving conversion efficiency within the existing funnel.

The analysis demonstrates how Business Intelligence techniques can transform customer behavior data into measurable actions that directly improve recurring revenue.
