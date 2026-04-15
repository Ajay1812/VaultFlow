-- stg_orders.sql
SELECT * FROM {{ source('vault_db', 'fact_orders') }}