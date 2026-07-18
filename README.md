# E-Commerce Data Pipeline

An end-to-end data engineering project that ingests, cleans, models, and analyzes e-commerce order data — built as a hands-on learning project covering the full pipeline lifecycle from raw data to a queryable warehouse.

## Overview

This project uses the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (orders, customers, order items, and products) to simulate a real-world data pipeline. The goal is to take scattered, raw CSV files and turn them into clean, joined, queryable data that could power business dashboards or analysis — while practicing the core skills of data engineering: ingestion, transformation, data modeling, and (eventually) orchestration.

## Tech Stack

- **Python** (pandas) — data loading, cleaning, and transformation
- **Jupyter Notebooks** (via VS Code) — exploratory data analysis
- **PostgreSQL** (Docker) — data warehouse
- **SQL** — data modeling (star schema) *(planned)*
- **Airflow / cron** — pipeline orchestration *(planned)*
- **Metabase** — dashboarding *(planned)*
- **Git/GitHub** — version control

## Project Structure
## Progress

- [x] Loaded raw CSVs (orders, customers, order_items, products) with pandas
- [x] Explored table relationships and joined them into a unified dataset
- [x] Ran initial business analysis (revenue, top categories, state-level trends)
- [x] Set up project structure and version control
- [x] Load data into PostgreSQL (Docker)
- [x] Build star schema (fact/dimension tables)
- [ ] Write reusable ETL script
- [ ] Automate pipeline (cron → Airflow)
- [ ] Build dashboard (Metabase)

## Key Findings So Far

- Total revenue across order items: ~R$13.6M
- Top-selling categories: bed/bath/table, beauty & health, sports & leisure
- São Paulo (SP) leads in both order volume and total revenue
- Paraíba (PB) has the highest *average* order value, despite lower volume — showing volume and value trends don't always align

## How to Run

1. Clone this repo
2. Download the [Olist dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and place the CSVs in `raw_data/`
3. Install dependencies: `pip install pandas jupyter sqlalchemy psycopg2-binary`
4. Run PostgreSQL locally via Docker
5. Open `notebooks/explore.ipynb` to run the exploration and load data into Postgres

*(Setup instructions will expand as the pipeline components are added.)*

## Author

Built by [Rohan Reddy](https://github.com/rohanreddy2601-dev) as a hands-on data engineering learning project.
## Star Schema

- **fact_order_items** — one row per item sold (order_id, product_id, customer_id, price, freight_value, purchase_date)
- **dim_customers** — customer_id, city, state
- **dim_products** — product_id, category, weight, dimensions
- **dim_date** — full calendar table (year, month, day, weekday) for time-based analysis