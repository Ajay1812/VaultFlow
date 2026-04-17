CREATE DATABASE airflow;
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE dim_locations (
	location_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	city          VARCHAR(100),
	state         VARCHAR(50),
	region        VARCHAR(50),
	pincode       VARCHAR(10),
	created_at    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE dim_dates (
	date_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	full_date     DATE,
	day           INT,
	month         INT,
	month_name    VARCHAR(20),
	quarter       INT,
	year          INT,
	created_at    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE dim_products (
	product_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	name          VARCHAR(100),
	category      VARCHAR(100),
	sub_category  VARCHAR(100),
	brand         VARCHAR(100),
	unit_price    NUMERIC(10,2),
	created_at    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE dim_customers (
	customer_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	name          VARCHAR(100),
	age           INT,
	phone         VARCHAR(50),
	email         VARCHAR(50),
	segment       VARCHAR(50),
	created_at    TIMESTAMP DEFAULT NOW(),
	location_id   UUID REFERENCES dim_locations(location_id)
);

CREATE TABLE fact_orders (
	order_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	customer_id   UUID REFERENCES dim_customers(customer_id),
	date_id       UUID REFERENCES dim_dates(date_id),
	product_id    UUID REFERENCES dim_products(product_id),
	location_id   UUID REFERENCES dim_locations(location_id),
	unit_price    NUMERIC(10,2),
	qty           INT,
	discount      NUMERIC(5,2),
	total_amount  NUMERIC(10,2),
	status        VARCHAR(30),
	created_at    TIMESTAMP DEFAULT NOW()
);