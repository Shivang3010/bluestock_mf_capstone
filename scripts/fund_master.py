import os
import pandas as pd

def explore_fund_master():
    file_path = os.path.join("data", "raw", "01_fund_master.csv")
    
    if not os.path.exists(file_path):
        print(f" Error: fund_master.csv not found at {file_path}")
        print("Please ensure your provided dataset is copied into that folder.")
        return

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    
    print("==================================================")
    print("        EXPLORING MUTUAL FUND MASTER DATA         ")
    print("==================================================\n")
    
    target_columns = {
        "fund_house": "Fund Houses (AMCs)",
        "category": "Broad Asset Categories",
        "sub_category": "Sub-Categories",
        "risk_grade": "Risk Profiles / Grades"
    }
    
    for col_name, friendly_label in target_columns.items():
        matched_col = [c for c in df.columns if col_name in c.lower() or col_name.replace("_", "") in c.lower()]
        
        if matched_col:
            actual_col = matched_col[0]
            unique_values = df[actual_col].dropna().unique()
            
            print(f"🔹 {friendly_label} (Total Unique: {len(unique_values)})")
            try:
                unique_values.sort()
            except:
                pass
            
            for val in unique_values:
                print(f"  • {val}")
            print("-" * 50)
        else:
            print(f" Column matching '{col_name}' not detected in fund_master.csv")
            print(f"   Available columns are: {list(df.columns)}")
            print("-" * 50)

if __name__ == "__main__":
    explore_fund_master()