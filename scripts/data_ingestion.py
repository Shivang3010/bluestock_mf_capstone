import os
import requests
import pandas as pd

def fetch_target_schemes():
    schemes = {
        "125497": "HDFC Top 100 Direct",
        "119551": "SBI Bluechip",
        "120503": "ICICI Bluechip",
        "118632": "Nippon Large Cap",
        "119092": "Axis Bluechip",
        "120841": "Kotak Bluechip"
    }
    
    output_dir = os.path.join("data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🚀 Starting Day 1 Live NAV Fetch for {len(schemes)} schemes...\n")
    
    for code, friendly_name in schemes.items():
        url = f"https://api.mfapi.in/mf/{code}"
        output_file = os.path.join(output_dir, f"nav_history_{code}.csv")
        
        print(f"Fetching data for: {friendly_name} (Code: {code})...")
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            json_data = response.json()
            meta_info = json_data.get("meta", {})
            nav_entries = json_data.get("data", [])
            
            if not nav_entries:
                print(f"⚠️ Warning: No historical data returned for {friendly_name}.")
                continue
                
            df = pd.DataFrame(nav_entries)
            
            df["scheme_code"] = meta_info.get("scheme_code", code)
            df["scheme_name"] = meta_info.get("scheme_name", friendly_name)
            
            df = df[["scheme_code", "scheme_name", "date", "nav"]]
            
            df.to_csv(output_file, index=False)
            print(f" Successfully saved {len(df)} rows -> {output_file}\n")
            
        except requests.exceptions.RequestException as e:
            print(f" Network/API Error for {friendly_name}: {e}\n")
        except Exception as e:
            print(f" Unexpected Error processing {friendly_name}: {e}\n")

    print("🏁 Data ingestion for all target schemes complete!")

if __name__ == "__main__":
    fetch_target_schemes()