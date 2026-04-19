-- stg_products.sql
SELECT * FROM {{ source('vault_db', 'dim_products') }}