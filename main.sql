WITH MatchStatus AS (
    SELECT 
        s.transaction_id,
        s.distributor_id,
        s.sales_amount,
        s.transaction_type,
        CASE 
            WHEN s.customer_id = 'MISSING_ID' THEN 'Exception: Missing ID'
            WHEN e.customer_id IS NULL THEN 'Exception: Unmapped ID'
            ELSE 'Confirmed Match'
        END AS reconciliation_status
    FROM stg_distributor_sales s
    LEFT JOIN erp_customer_master e 
        ON s.customer_id = e.customer_id
)

-- Generate the Executive Baseline Metrics
SELECT 
    reconciliation_status,
    COUNT(transaction_id) AS total_records,
    SUM(ABS(sales_amount)) AS gross_value_exposure,
    ROUND((COUNT(transaction_id) * 100.0 / (SELECT COUNT(*) FROM MatchStatus)), 2) AS pct_of_total_volume
FROM MatchStatus
GROUP BY reconciliation_status
ORDER BY gross_value_exposure DESC;