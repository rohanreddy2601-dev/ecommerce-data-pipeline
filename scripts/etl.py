import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="C:/Users/HP/OneDrive/Desktop/ecommerce-pipeline/.env")

# --- Configuration ---
RAW_DATA_PATH = "C:/Users/HP/OneDrive/Desktop/ecommerce-pipeline/raw_data"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ecommerce"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

print("Starting ETL pipeline...")
# --- Extract: Load raw CSVs ---
print("Loading CSVs...")

orders = pd.read_csv(f"{RAW_DATA_PATH}/olist_orders_dataset.csv")
customers = pd.read_csv(f"{RAW_DATA_PATH}/olist_customers_dataset.csv")
order_items = pd.read_csv(f"{RAW_DATA_PATH}/olist_order_items_dataset.csv")
products = pd.read_csv(f"{RAW_DATA_PATH}/olist_products_dataset.csv")

print(f"Loaded {len(orders)} orders, {len(customers)} customers, {len(order_items)} order items, {len(products)} products")
# --- Load: Push raw tables into Postgres ---
print("Loading raw tables into Postgres...")

orders.to_sql("orders", engine, if_exists="replace", index=False)
customers.to_sql("customers", engine, if_exists="replace", index=False)
order_items.to_sql("order_items", engine, if_exists="replace", index=False)
products.to_sql("products", engine, if_exists="replace", index=False)

print("Raw tables loaded.")
# --- Transform: Build star schema ---
print("Building star schema...")

with engine.connect() as conn:
    # dim_customers
    conn.execute(text("DROP TABLE IF EXISTS dim_customers;"))
    conn.execute(text("""
        CREATE TABLE dim_customers AS
        SELECT DISTINCT customer_id, customer_city, customer_state
        FROM customers;
    """))

    # dim_products
    conn.execute(text("DROP TABLE IF EXISTS dim_products;"))
    conn.execute(text("""
        CREATE TABLE dim_products AS
        SELECT DISTINCT product_id, product_category_name,
               product_weight_g, product_length_cm, product_height_cm, product_width_cm
        FROM products;
    """))

    # fact_order_items
    conn.execute(text("DROP TABLE IF EXISTS fact_order_items;"))
    conn.execute(text("""
        CREATE TABLE fact_order_items AS
        SELECT
            oi.order_id, oi.order_item_id, o.customer_id, oi.product_id,
            oi.price, oi.freight_value, o.order_purchase_timestamp::date AS purchase_date
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id;
    """))

    # dim_date
    conn.execute(text("DROP TABLE IF EXISTS dim_date;"))
    conn.execute(text("""
        CREATE TABLE dim_date AS
        SELECT
            d::date AS date,
            EXTRACT(YEAR FROM d) AS year,
            EXTRACT(MONTH FROM d) AS month,
            EXTRACT(DAY FROM d) AS day,
            TO_CHAR(d, 'Day') AS weekday_name,
            EXTRACT(DOW FROM d) AS weekday_number
        FROM generate_series(
            (SELECT MIN(purchase_date) FROM fact_order_items),
            (SELECT MAX(purchase_date) FROM fact_order_items),
            '1 day'
        ) AS d;
    """))

    conn.commit()

print("Star schema built successfully.")
print("ETL pipeline complete!")