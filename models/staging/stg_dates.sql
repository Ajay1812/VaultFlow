-- stg_dates.sql
SELECT * FROM {{ source('vault_db', 'dim_dates') }}