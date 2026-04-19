WITH grp_by_region AS (
	SELECT 
		a.customer_id,
		c.region,
		SUM(total_amount) AS amount_by_region
	FROM {{ ref('stg_orders') }} a
	JOIN {{ ref('stg_customers') }} b
	ON a.customer_id = b.customer_id
	JOIN {{ ref('stg_locations') }} c ON c.location_id = a.location_id
	GROUP BY a.customer_id, c.region
),
region_t AS (
SELECT
	*,
	RANK() OVER(PARTITION BY region ORDER BY amount_by_region DESC) AS rn
FROM grp_by_region a
)

SELECT * FROM region_t
WHERE rn <= 5
