
SELECT 
	b.category,
	SUM(a.total_amount) AS revenue
FROM {{ ref('stg_orders') }} a
JOIN {{ ref('stg_products') }}  b
ON a.product_id = b.product_id
GROUP BY b.category
ORDER BY revenue DESC