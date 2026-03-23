# MedSupply Demand Forecasting

## Live app 
https://medsupply-demand-nshnoft2b2ypv4hsjyxamy.streamlit.app/

## Overview
This project builds an end-to-end demand forecasting pipeline for pharmaceutical products using historical daily sales data. The goal is to predict next-day demand using time-series feature engineering and machine learning.

## Problem Statement
Healthcare and pharmaceutical supply chains require accurate demand forecasts to reduce stockouts, avoid overstocking, and improve inventory planning. In this project, I used historical product-wise demand data to forecast the next day's sales.

## Dataset
The project uses the `salesdaily.csv` file from the Pharma Sales dataset.

Features available in the raw data:
- date
- product category sales columns
- Year
- Month
- Weekday Name

The data was transformed from wide format to long format to create a product-level daily demand table.

## Project Workflow

### 1. Data Ingestion
- Loaded raw CSV data
- Stored raw data in SQLite
- Transformed daily sales data into a clean long-format sales table

### 2. SQL Analysis
Performed SQL-based analysis for:
- total demand by product
- monthly demand trends
- weekday demand patterns
- moving averages
- spike detection

### 3. Exploratory Data Analysis
- total daily demand trend
- product-wise demand comparison
- monthly seasonality
- weekday patterns
- outlier detection
- correlation analysis

### 4. Feature Engineering
Created time-series features such as:
- lag_1, lag_2, lag_3, lag_7
- rolling_3, rolling_7, rolling_14
- rolling_std_7
- day_of_week
- month
- day_of_month
- week_of_year
- is_weekend
- expanding_mean

Also:
- handled outliers using capping
- one-hot encoded product categories
- used shifted target to avoid data leakage

### 5. Model Building
Compared:
- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

Used a time-based train-test split instead of random split.

### 6. Model Validation
The final tuned Gradient Boosting model outperformed the naive baseline.

#### Final model performance
- MAE: ~3.26
- RMSE: ~5.20
- R²: ~0.77

#### Naive baseline
- MAE: ~4.30

Final model: Tuned Gradient Boosting
MAE: ~3.26
RMSE: ~5.20
R²: ~0.77
Improvement over naive baseline: ~24%

This shows the ML model achieved roughly 24% improvement over the baseline.

## Key Insights
- Demand shows weekly seasonality
- Some products contribute disproportionately to total error
- Outlier handling improved model stability
- Feature engineering had more impact than model complexity
- Gradient Boosting performed best overall

