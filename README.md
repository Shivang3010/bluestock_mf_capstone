# Bluestock Mutual Fund Capstone Project

## Day 1: Data Ingestion & Quality Assessment Summary

### 📊 Data Quality Summary Report

**1. Data Ingestion Overview**
* **Source Systems:** `mfapi.in` REST API (Live JSON Payloads), `01_fund_master.csv` file asset.
* **Schemes Ingested:** All 6 core target funds (HDFC, SBI, ICICI, Nippon, Axis, Kotak Bluechip series) ingested successfully and converted from JSON into raw table format within `data/raw/` folder.

**2. Schema/Structure Validation**
* **File Structure Verification:** All ingested history files align perfectly to specified schema, where columns include `scheme_code`, `scheme_name`, `date`, `nav`.
* **Consistent Data Types:** `date` field data universally consistent with string data type (`DD-MM-YYYY`), `nav` isolated safely as numeric value within JSON array.

**3. Referential Integrity Assessment (AMFI Validation)**
* **Completeness Test:** Cross-checked primary keys within `01_fund_master.csv` file against filenames within `data/raw/`.
* **Integrity Status:** Pass. 100% of mutual fund scheme records within our system map reliably to one unique file entry.