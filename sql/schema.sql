PRAGMA foreign_keys = ON;
CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_name TEXT NOT NULL,
    category TEXT NOT NULL,
    risk_level TEXT,
    fund_house TEXT NOT NULL
);

CREATE TABLE dim_date (
    date_id TEXT PRIMARY KEY, 
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    is_weekend INTEGER NOT NULL CHECK (is_weekend IN (0, 1))
);
CREATE TABLE fact_nav (
    amfi_code INTEGER,
    date TEXT,
    nav REAL NOT NULL,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund (amfi_code) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (date) REFERENCES dim_date (date_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id INTEGER NOT NULL,
    amfi_code INTEGER,
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('SIP', 'Lumpsum', 'Redemption')),
    amount REAL NOT NULL CHECK (amount > 0),
    transaction_date TEXT,
    state TEXT,
    kyc_status TEXT NOT NULL CHECK (kyc_status IN ('Verified', 'Pending', 'Failed')),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund (amfi_code)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (transaction_date) REFERENCES dim_date (date_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE TABLE fact_performance (
    amfi_code INTEGER PRIMARY KEY,
    return_1y REAL,
    return_3y REAL,
    return_5y REAL,
    expense_ratio REAL CHECK (expense_ratio >= 0.1 AND expense_ratio <= 2.5),
    is_anomaly INTEGER NOT NULL CHECK (is_anomaly IN (0, 1)),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund (amfi_code)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE fact_aum (
    amfi_code INTEGER,
    as_of_date TEXT,
    aum_amount REAL NOT NULL CHECK (aum_amount >= 0),
    PRIMARY KEY (amfi_code, as_of_date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund (amfi_code)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (as_of_date) REFERENCES dim_date (date_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_transactions_date ON fact_transactions(transaction_date);
CREATE INDEX idx_transactions_fund ON fact_transactions(amfi_code);
CREATE INDEX idx_nav_date ON fact_nav(date);