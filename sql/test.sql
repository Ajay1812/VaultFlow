SELECT * FROM dim_locations;

SELECT * FROM dim_dates;

SELECT * FROM dim_products;

SELECT * FROM dim_customers;

SELECT * FROM fact_orders;

SELECT COUNT(*) FROM dim_locations;
SELECT COUNT(*) FROM dim_dates;
SELECT COUNT(*) FROM dim_products;
SELECT COUNT(*) FROM dim_customers;
SELECT COUNT(*) FROM fact_orders;

-- TRUNCATE TABLE fact_orders, dim_customers, dim_products, dim_dates, dim_locations;