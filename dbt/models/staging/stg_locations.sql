-- stg_locations.sql
SELECT * FROM {{ source('vault_db', 'dim_locations') }}