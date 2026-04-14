-- stg_dates.sql
SELECT * FROM {{ source('retail_db', 'dim_dates') }}