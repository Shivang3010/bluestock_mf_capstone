import sqlite3
import pandas as pd
import numpy as np

def init_database():
    conn = sqlite3.connect('mutual_fund_analytics.db')
    cursor = conn.cursor()
    
    print("Creating database schema...")
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dim_Schemes (
        Scheme_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        AMFI_Code INT UNIQUE,
        Scheme_Name TEXT,
        Category TEXT,
        Fund_House TEXT
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dim_Investors (
        Investor_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Age INT,
        Age_Group TEXT,
        Gender TEXT,
        State TEXT,
        City_Tier TEXT
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Fact_NAV_History (
        Fact_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        AMFI_Code INT,
        NAV REAL,
        FOREIGN KEY(AMFI_Code) REFERENCES Dim_Schemes(AMFI_Code)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Fact_SIP_Inflows (
        Month_Year TEXT PRIMARY KEY,
        SIP_Inflow_Cr REAL,
        Net_Category_Inflow_Cr REAL,
        Folio_Count_Cr REAL
    )''')
    
    conn.commit()
    return conn

def seed_mock_data(conn):
    print("Generating and seeding cleaned validation data...")
    dates = pd.date_range(start="2022-01-01", end="2026-03-31", freq="D").strftime('%Y-%m-%d').tolist()
    months = pd.date_range(start="2022-01-01", end="2025-12-31", freq="ME").strftime('%Y-%m').tolist()
    
    categories = ['Large Cap', 'Mid Cap', 'Small Cap', 'Flexi Cap', 'Sectoral']
    amcs = ['SBI Mutual Fund', 'HDFC Mutual Fund', 'ICICI Prudential MF', 'Axis Mutual Fund', 'Quant Mutual Fund']
    
    schemes_data = []
    for i in range(1, 41):
        schemes_data.append((100000 + i, f"Scheme {i}", categories[i % 5], amcs[i % 5]))
    
    cursor = conn.cursor()
    cursor.executemany("INSERT OR IGNORE INTO Dim_Schemes (AMFI_Code, Scheme_Name, Category, Fund_House) VALUES (?, ?, ?, ?)", schemes_data)
    
    nav_data = []
    for amfi, _, _, _ in schemes_data:
        base_nav = np.random.uniform(10, 100)
        for date in dates:
            year = date[:4]
            if year == '2023':
                change = np.random.uniform(-0.002, 0.008)
            elif year == '2024':
                change = np.random.uniform(-0.007, 0.003)
            else:
                change = np.random.uniform(-0.004, 0.005)
            base_nav *= (1 + change)
            nav_data.append((date, amfi, round(base_nav, 4)))
            
    cursor.executemany("INSERT INTO Fact_NAV_History (Date, AMFI_Code, NAV) VALUES (?, ?, ?)", nav_data)
    
    sip_data = []
    start_sip = 13000
    start_folios = 13.26
    
    for idx, month in enumerate(months):
        pct_progress = idx / len(months)
        sip_val = start_sip + (31002 - start_sip) * (pct_progress ** 1.2) + np.random.uniform(-300, 300)
        folio_val = start_folios + (26.12 - start_folios) * pct_progress + np.random.uniform(-0.1, 0.1)
        if month == '2025-12':
            sip_val = 31002
            folio_val = 26.12
        sip_data.append((month, round(sip_val, 2), round(sip_val * np.random.uniform(0.6, 1.4), 2), round(folio_val, 2)))
        
    cursor.executemany("INSERT OR IGNORE INTO Fact_SIP_Inflows (Month_Year, SIP_Inflow_Cr, Net_Category_Inflow_Cr, Folio_Count_Cr) VALUES (?, ?, ?, ?)", sip_data)
    
    genders = ['Male', 'Female', 'Other']
    states = ['Maharashtra', 'Gujarat', 'Karnataka', 'Delhi', 'Tamil Nadu', 'West Bengal']
    age_groups = ['18-25', '26-35', '36-45', '46-60', '60+']
    
    investor_data = []
    for _ in range(1000):
        age = int(np.random.normal(38, 12))
        age = max(18, min(age, 80))
        if age <= 25: ag = '18-25'
        elif age <= 35: ag = '26-35'
        elif age <= 45: ag = '36-45'
        elif age <= 60: ag = '46-60'
        else: ag = '60+'
        
        investor_data.append((
            age, ag, np.random.choice(genders, p=[0.60, 0.38, 0.02]),
            np.random.choice(states), np.random.choice(['T30', 'B30'], p=[0.72, 0.28])
        ))
    cursor.executemany("INSERT INTO Dim_Investors (Age, Age_Group, Gender, State, City_Tier) VALUES (?, ?, ?, ?, ?)", investor_data)
    
    conn.commit()
    print("Database preparation and parsing complete!")

if __name__ == "__main__":
    connection = init_database()
    seed_mock_data(connection)
    connection.close()