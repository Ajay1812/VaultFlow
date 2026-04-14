-- stg_customers.sql
SELECT * FROM {{ source('retail_db', 'dim_customers') }}