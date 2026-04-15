-- stg_customers.sql
SELECT * FROM {{ source('vault_db', 'dim_customers') }}