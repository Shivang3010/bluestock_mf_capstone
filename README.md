## 📌 Project Overview
This repository contains the end-to-end data engineering pipeline and quantitative analytics engine engineered for the Bluestock Fintech Capstone initiative. The architecture automates the daily ingestion, cleansing, transformation, and statistical profiling of all active domestic mutual fund variants operating across the Indian capital markets. 

By abstracting away the structural fragmentation of raw public market feeds (such as AMFI clearings), the system delivers an indexed, unified, and programmatically queryable data layer optimized for algorithmic advisory systems and modern portfolio theory (MPT) evaluation.

---

## 🏗️ Architecture Design (Medallion Pattern)
The pipeline is designed using the enterprise Medallion Architecture pattern to ensure strict data governance, validation boundaries, and auditability:

1. **Bronze (Staging Tier):** Asynchronous extraction of unformatted, semi-colon delimited flat-file text streams directly from AMFI endpoints and secondary RESTful APIs.
2. **Silver (Curated Tier):** Vectorized data sanitation utilizing Python `pandas`. This stage handles schema enforcement, isolates missing information ("N.A." strings), standardizes dates to ISO 8601, and filters out duplicate records.
3. **Gold (Analytical Tier):** Materialized relational tables optimized for fast BI dashboard consumption, handling calculated rolling historical windows, drawdown tracking metrics, and portfolio risk calculations.

---

## 📊 Core Datasets & Source Mapping
The processing core unifies data across multiple structural domains:
* **AMFI Scheme Master Feed:** Daily End-of-Day (EOD) Net Asset Value (NAV) files, unique scheme codes, and ISIN tracking indicators.
* **Market Benchmarks:** Historical dividend-adjusted daily close records for the Nifty 50 and Nifty Midcap 100 indices pulled via the `yfinance` API.
* **Longitudinal History:** Multi-year time-series data extracted from secondary RESTful gateways for multi-variant covariance and rolling Sharpe ratio profiling.

---

## 🧮 Embedded Quantitative Metrics
The engine automatically computes risk-adjusted metrics over rolling windows using classical Modern Portfolio Theory (MPT) frameworks:
* **Jensen's Alpha ($\alpha$):** Measures pure structural outperformance relative to a baseline CAPM model.
* **Systemic Market Beta ($\beta$):** Tracks volatility sensitivity relative to primary sovereign benchmarks.
* **Sharpe Efficiency Ratio:** Quantifies risk-adjusted return parameters per unit of localized volatility.

---

## 🚀 Getting Started & Execution

### 1. Prerequisites & Environment Setup
Clone the repository and install the verified core dependencies:
```bash
git clone [https://github.com/your-username/bluestock-mf-capstone.git](https://github.com/your-username/bluestock-mf-capstone.git)
cd bluestock-mf-capstone
pip install -r requirements.txt
