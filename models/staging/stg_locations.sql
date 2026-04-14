-- stg_locations.sql
SELECT * FROM {{ source('retail_db', 'dim_locations') }}