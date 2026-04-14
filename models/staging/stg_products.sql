-- stg_products.sql
SELECT * FROM {{ source('retail_db', 'dim_products') }}