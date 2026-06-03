SELECT 
    amfi_code,
    aum_amount AS aum_in_crores,
    as_of_date
FROM fact_aum
ORDER BY aum_amount DESC
LIMIT 5;

SELECT 
    amfi_code, 
    strftime('%Y-%m', date) AS production_month, 
    ROUND(AVG(nav), 4) AS average_monthly_nav
FROM fact_nav
GROUP BY amfi_code, production_month
ORDER BY amfi_code, production_month;

WITH sip_yearly_ledger AS (
    SELECT 
        strftime('%Y', transaction_date) AS fiscal_year, 
        SUM(amount) AS absolute_sip_volume
    FROM fact_transactions
    WHERE transaction_type = 'SIP'
    GROUP BY fiscal_year
)
SELECT 
    curr.fiscal_year, 
    curr.absolute_sip_volume AS current_year_volume,
    prev.absolute_sip_volume AS previous_year_volume,
    ROUND(((curr.absolute_sip_volume - prev.absolute_sip_volume) / prev.absolute_sip_volume) * 100, 2) AS yoy_growth_percentage
FROM sip_yearly_ledger curr
LEFT JOIN sip_yearly_ledger prev 
    ON CAST(curr.fiscal_year AS INT) = CAST(prev.fiscal_year AS INT) + 1
ORDER BY curr.fiscal_year;

SELECT 
    state, 
    COUNT(transaction_id) AS transaction_count, 
    ROUND(SUM(amount), 2) AS total_capital_injected
FROM fact_transactions
GROUP BY state
ORDER BY total_capital_injected DESC;

SELECT 
    amfi_code, 
    ROUND(expense_ratio, 2) AS asset_expense_ratio_pct
FROM fact_performance
WHERE expense_ratio < 1.0
ORDER BY expense_ratio ASC;

SELECT 
    ROUND(SUM(CASE WHEN transaction_type IN ('SIP', 'Lumpsum') THEN amount ELSE 0 END), 2) AS total_gross_inflow,
    ROUND(SUM(CASE WHEN transaction_type = 'Redemption' THEN amount ELSE 0 END), 2) AS total_gross_outflow,
    ROUND(SUM(CASE WHEN transaction_type IN ('SIP', 'Lumpsum') THEN amount ELSE 0 END) - 
          SUM(CASE WHEN transaction_type = 'Redemption' THEN amount ELSE 0 END), 2) AS net_retained_liquidity
FROM fact_transactions;

SELECT 
    amfi_code, 
    return_1y, 
    expense_ratio
FROM fact_performance
WHERE is_anomaly = 1
ORDER BY return_1y DESC;

SELECT 
    amfi_code,
    return_3y AS compound_annual_return_3yr,
    expense_ratio
FROM fact_performance
WHERE return_3y > 15.0
ORDER BY return_3y DESC;

SELECT 
    kyc_status, 
    COUNT(*) AS absolute_transaction_count, 
    ROUND(SUM(amount), 2) AS locked_monetary_value
FROM fact_transactions
GROUP BY kyc_status
ORDER BY locked_monetary_value DESC;

WITH ordered_nav_sequence AS (
    SELECT 
        amfi_code, 
        nav, 
        date,
        ROW_NUMBER() OVER (PARTITION BY amfi_code ORDER BY date ASC) as point_baseline_rank,
        ROW_NUMBER() OVER (PARTITION BY amfi_code ORDER BY date DESC) as point_latest_rank
    FROM fact_nav
)
SELECT 
    base.amfi_code, 
    base.nav AS historic_base_nav, 
    curr.nav AS current_latest_nav,
    ROUND(((curr.nav - base.nav) / base.nav) * 100, 2) AS absolute_lifetime_growth_pct
FROM (SELECT amfi_code, nav FROM ordered_nav_sequence WHERE point_baseline_rank = 1) base
JOIN (SELECT amfi_code, nav FROM ordered_nav_sequence WHERE point_latest_rank = 1) curr 
    ON base.amfi_code = curr.amfi_code
ORDER BY absolute_lifetime_growth_pct DESC;