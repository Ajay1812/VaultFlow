SELECT 
	b.month,
	b.month_name,
	SUM(a.total_amount) AS monthly_sales
FROM {{ ref('stg_orders') }} a
JOIN {{ ref('stg_dates') }}  b
ON a.date_id = b.date_id
GROUP BY b.month, b.month_name
ORDER BY b.month
