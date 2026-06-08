import os
import glob
import pandas as pd

def validate_amfi_codes():
    fund_master_path = os.path.join("data", "raw", "01_fund_master.csv")
    raw_data_dir = os.path.join("data", "raw")
    
    if not os.path.exists(fund_master_path):
        print(f" Error: fund_master.csv not found at {fund_master_path}")
        return

    df_master = pd.read_csv(fund_master_path, dtype=str)
    df_master.columns = df_master.columns.str.strip()
    
    code_col = [c for c in df_master.columns if "code" in c.lower() or "amfi" in c.lower()][0]
    master_codes = set(df_master[code_col].str.strip().unique())

    csv_files = glob.glob(os.path.join(raw_data_dir, "nav_history_125497*.csv"))
    downloaded_codes = set()
    
    for file_path in csv_files:
        filename = os.path.basename(file_path)
        code_from_file = filename.replace("nav_history_", "").replace(".csv", "")
        downloaded_codes.add(code_from_file)

    matched_codes = master_codes.intersection(downloaded_codes)
    missing_in_nav = master_codes - downloaded_codes
    unexpected_nav = downloaded_codes - master_codes

    print("==================================================")
    print("         AMFI CODE VALIDATION REPORT              ")
    print("==================================================")
    print(f" Total Unique AMFI Codes in Master File : {len(master_codes)}")
    print(f" Total Active NAV Files in Raw Directory: {len(downloaded_codes)}")
    print(f" Successfully Matched Code Mappings    : {len(matched_codes)}")
    print(f" Missing NAV Records (In Master only)  : {len(missing_in_nav)}")
    print(f" Orphaned NAV Records (In Directory only): {len(unexpected_nav)}")
    print("--------------------------------------------------")
    
    if len(missing_in_nav) == 0:
        print(" Integrity Check: PASSED. All master codes match historical logs.")
    else:
        print(f" Integrity Check: WARNING. {len(missing_in_nav)} codes lack matching files.")
        print(f"   Sample Missing Codes: {list(missing_in_nav)[:5]}")
    print("==================================================")

if __name__ == "__main__":
    validate_amfi_codes()