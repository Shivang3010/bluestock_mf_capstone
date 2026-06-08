import os
import requests
import pandas as pd

def fetch_live_nav():
    scheme_code = "125497"
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    
    output_dir = os.path.join("data", "raw")
    output_file = os.path.join(output_dir, f"nav_history_{scheme_code}.csv")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Connecting to API endpoint: {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        json_data = response.json()
        
        meta_info = json_data.get("meta", {})
        nav_entries = json_data.get("data", [])
        
        if not nav_entries:
            print(f"Error: No NAV data found inside the response payload.")
            return
            
        df = pd.DataFrame(nav_entries)
        
        df["scheme_code"] = meta_info.get("scheme_code", scheme_code)
        df["scheme_name"] = meta_info.get("scheme_name", "HDFC Top 100 Direct Plan - Growth")
        
        df = df[["scheme_code", "scheme_name", "date", "nav"]]
        
        df.to_csv(output_file, index=False)
        print(f"Successfully processed {len(df)} rows.")
        print(f"Raw CSV generated successfully at: {output_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"API Connection Failed: {e}")
    except Exception as e:
        print(f"An unexpected parsing issue occurred: {e}")

if __name__ == "__main__":
    fetch_live_nav()