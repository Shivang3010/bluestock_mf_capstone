# BlueStock Mutual Fund Analytics — Data Dictionary

This document provides a comprehensive breakdown of the logical star schema designed for the BlueStock Mutual Fund Analytics database (`bluestock_mf.db`). It serves as a data governance guide documenting all system entities, data tracking specifications, and source lineage.

---

## 1. Schema Architecture Overview

The database leverages a star schema optimization strategy to separate transactional data metrics from relational attribute contexts. 

* **Dimension Tables:** Maintain tracking contexts (Funds, Dates).
* **Fact Tables:** Track granular transactional ledgers, structural performance indicators, historical time-series pricing (NAV), and periodic asset balances (AUM).

---

## 2. Dimensional Entities

### Table: `dim_fund`
* **Business Definition:** The primary data master directory storing reference attributes and organizational classifications for all mutual fund schemas managed across the platform.
* **Source Reference:** Ingested from reference operational masters matching valid global registration indexes.

| Column Name | Storage Type | Key / Constraint | Business Definition & Validation Rules |
| :--- | :--- | :--- | :--- |
| `amfi_code` | `INTEGER` | PRIMARY KEY | Unique Association of Mutual Funds in India (AMFI) identification index assigned to each fund. |
| `fund_name` | `TEXT` | NOT NULL | Complete commercial marketing name of the mutual fund scheme. |
| `category` | `TEXT` | NOT NULL | Core operational investment asset class strategy (e.g., Equity, Debt, Hybrid, Liquid). |
| `risk_level` | `TEXT` | None | Risk-o-meter category classification profile (e.g., Low, Moderate, High, Very High). |
| `fund_house` | `TEXT` | NOT NULL | The Asset Management Company (AMC) responsible for launching and administering the fund asset pool. |

---

### Table: `dim_date`
* **Business Definition:** A standardized time dimension containing explicit fiscal and seasonal calendar breakdowns to streamline time-series grouping and eliminate slow runtime string manipulation functions.
* **Source Reference:** System-generated calendar table.

| Column Name | Storage Type | Key / Constraint | Business Definition & Validation Rules |
| :--- | :--- | :--- | :--- |
| `date_id` | `TEXT` | PRIMARY KEY | Standalone unique date index formatted explicitly as an ISO-8601 string (`YYYY-MM-DD`). |
| `year` | `INTEGER` | NOT NULL | Full 4-digit calendar year index (e.g., 2026). |
| `month` | `INTEGER` | NOT NULL | Calendar month index representation ranging sequentially from `1` (January) to `12` (December). |
| `day` | `INTEGER` | NOT NULL | Sequential numerical index representing the day of the current month (`1` to `31`). |
| `quarter` | `INTEGER` | NOT NULL | Annual corporate fiscal tracking quarter value (`1` through `4`). |
| `is_weekend` | `INTEGER` | CHECK (0, 1) | Binary classification flag indicating if the specific date falls on a weekend; `1` for Saturday/Sunday, `0` for weekdays. |

---

## 3. Analytical Fact Tables

### Table: `fact_nav`
* **Business Definition:** A continuous daily historical record logging the price per share unit (Net Asset Value) of every registered mutual fund.
* **Source Reference:** Processed from raw data logs (`02_nav_history.csv`).

| Column Name | Storage Type | Key / Constraint | Business Definition & Validation Rules |
| :--- | :--- | :--- | :--- |
| `amfi_code` | `INTEGER` | COMPOSITE PK / FK | Target index pointing back to the relational `dim_fund(amfi_code)` schema. |
| `date` | `TEXT` | COMPOSITE PK / FK | Target timestamp day mapped explicitly back to `dim_date(date_id)`. |
| `nav` | `REAL` | NOT NULL | Net Asset Value pricing evaluation per unit. Cleaned via forward-fill (`.ffill()`) grouping to carry closing prices across weekend or holiday market closures. Validated to ensure values are strictly $> 0$. |

---

### Table: `fact_transactions`
* **Business Definition:** The central financial ledger containing all itemized purchase, recurring allotment, and liquidity withdrawal requests submitted by retail investors.
* **Source Reference:** Cleansed and normalized from transaction logs (`08_investor_transactions.csv`).

| Column Name | Storage Type | Key / Constraint | Business Definition & Validation Rules |
| :--- | :--- | :--- | :--- |
| `transaction_id` | `INTEGER` | PRIMARY KEY | Internal system auto-incrementing surrogate index used to identify individual ledger entries. |
| `investor_id` | `INTEGER` | NOT NULL | Masked, anonymized reference token representing a unique client account. |
| `amfi_code` | `INTEGER` | FOREIGN KEY | Target schema connector linked to `dim_fund(amfi_code)`. |
| `transaction_type`| `TEXT` | CHECK (Enum) | Standardized entry method description mapped exclusively into three valid enum string types: `SIP`, `Lumpsum`, or `Redemption`. |
| `amount` | `REAL` | CHECK ($> 0$) | Total fiat valuation volume processed in Indian Rupees (INR). Remapped from the original `amount_inr` field and strictly validated to filter out empty, negative, or zero balances. |
| `transaction_date`| `TEXT` | FOREIGN KEY | Operational tracking link pointing back to `dim_date(date_id)`. |
| `state` | `TEXT` | None | Geographic region tracking indicator tracking the investor's domestic physical point of origin. |
| `kyc_status` | `TEXT` | CHECK (Enum) | Current operational compliance flag mapped explicitly as: `Verified`, `Pending`, or `Failed`. Non-matching inputs fall back to `Pending`. |

---

### Table: `fact_performance`
* **Business Definition:** Annualized, multi-window compound growth rate summaries and operational maintenance expenses mapped per fund to assess investment efficiency.
* **Source Reference:** Transformed from performance analytical metrics (`07_scheme_performance.csv`).

| Column Name | Storage Type | Key / Constraint | Business Definition & Validation Rules |
| :--- | :--- | :--- | :--- |
| `amfi_code` | `INTEGER` | PRIMARY KEY / FK | Relational primary key linked directly 1-to-1 with `dim_fund(amfi_code)`. |
| `return_1y` | `REAL` | None | Rolling 1-year total absolute percentage return performance. Remapped from `return_1yr_pct`. |
| `return_3y` | `REAL` | None | 3-year trailing Compound Annual Growth Rate percentage (CAGR). Remapped from `return_3yr_pct`. |
| `return_5y` | `REAL` | None | 5-year trailing Compound Annual Growth Rate percentage (CAGR). Remapped from `return_5yr_pct`. |
| `expense_ratio` | `REAL` | CHECK Range | Total percentage of fund assets diverted annually to cover operating management fees. Remapped from `expense_ratio_pct` and capped inside standard institutional bounds ($0.1\% \le x \le 2.5\%$). |
| `is_anomaly` | `INTEGER` | CHECK (0, 1) | Data sanity flag. Set to `1` if short-term yields demonstrate high volatility or extreme tracking parameters (where `return_1y` $> 100\%$ or $< -50\%$). Defaults to `0`. |

---

### Table: `fact_aum`
* **Business Definition:** Periodic institutional point-in-time snapshot ledger records capturing total cumulative net valuation balances under active corporate management.
* **Source Reference:** Dynamically generated from asset metrics embedded inside `07_scheme_performance.csv`.

| Column Name | Storage Type | Key / Constraint | Business Definition & Validation Rules |
| :--- | :--- | :--- | :--- |
| `amfi_code` | `INTEGER` | COMPOSITE PK / FK | Reference database schema connector linked to `dim_fund(amfi_code)`. |
| `as_of_date` | `TEXT` | COMPOSITE PK / FK | Target date record tracking when the AUM snapshot calculation was officially logged. |
| `aum_amount` | `REAL` | CHECK ($\ge 0$) | Net asset valuation metric calculated and tracked explicitly in Crores (INR). Remapped from raw column entry `aum_crore`. |