import os
import pandas as pd
from sqlalchemy import create_engine, text

DB_PATH = "bluestock_mf.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

PROCESSED_DATA_MAP = {
    "fact_nav": "data/processed/nav_history_clean.csv",
    "fact_transactions": "data/processed/investor_transactions_clean.csv",
    "fact_performance": "data/processed/scheme_performance_clean.csv"
}

def load_and_verify_all():
    print("🚀 Initiating Database Load & Row Verification Engine...\n" + "="*60)
    
    all_passed = True
    verification_summary = []
    
    for table_name, csv_path in PROCESSED_DATA_MAP.items():
        if not os.path.exists(csv_path):
            print(f"❌ Error: Cleansed source file not found at '{csv_path}'. Run cleaning step first.")
            all_passed = False
            continue
            
        df = pd.read_csv(csv_path)
        csv_row_count = len(df)
        
        df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
        print(f"📥 Streamed '{csv_path}' -> SQLite table '{table_name}'")
        
        with engine.connect() as connection:
            query = text(f"SELECT COUNT(*) FROM {table_name};")
            db_row_count = connection.execute(query).scalar()
            
        status = "✅ PASSED" if csv_row_count == db_row_count else "❌ FAILED"
        if csv_row_count != db_row_count:
            all_passed = False
            
        verification_summary.append({
            "Table Name": table_name,
            "Cleaned CSV Rows": csv_row_count,
            "SQLite DB Rows": db_row_count,
            "Status": status
        })
        
    print("\n" + "="*60)
    print("📋 ROW INTEGRITY VERIFICATION REPORT")
    print("="*60)
    print(f"{'Target Table':<20} | {'CSV Rows':<10} | {'Database Rows':<15} | {'Verification Status'}")
    print("-" * 65)
    for entry in verification_summary:
        print(f"{entry['Table Name']:<20} | {entry['Cleaned CSV Rows']:<10} | {entry['SQLite DB Rows']:<15} | {entry['Status']}")
    print("="*60)
    
    if all_passed:
        print("🎉 Success! All rows loaded completely. Row audit checks show a perfect match.")
    else:
        print("⚠️ Warning: Data mismatch detected during row verification audit. Check logs above.")

if __name__ == "__main__":
    load_and_verify_all()