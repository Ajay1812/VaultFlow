-- stg_orders.sql
SELECT * FROM {{ source('retail_db', 'fact_orders') }}