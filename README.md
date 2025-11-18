# 📊 Vendor Performance Analysis
# Overview
This project combines Python, SQL, and Power BI to deliver a comprehensive Vendor Performance Analysis for the retail and wholesale sector. It demonstrates an end-to-end workflow — from data ingestion and transformation to visual analytics and KPI dashboards — to identify top-performing vendors, underperforming brands, and opportunities to optimize procurement and pricing decisions.

# Business Problem
In retail and wholesale, profitability can be eroded by poor pricing, inefficient vendor management, and slow inventory turnover.\
This project addresses those challenges by:\
🏷️ Identifying underperforming brands needing promotional or pricing adjustments.\
💰 Highlighting top vendors driving sales and gross profit.\
📦 Analyzing how bulk purchasing impacts unit costs.\
🔄 Evaluating inventory turnover to reduce holding costs.\
📈 Assessing profitability variance between high- and low-performing vendors.\

# Project Structure
Vendor-Performance-Analysis/\
│\
├── ingestion_db.py                     # Ingests CSVs into SQLite database\
├── get_vendor_summary.py               # Script to get cleaned vendor summary table and ingest into database\
├── Exploratory Data Analysis.ipynb     # Python-based analysis and insights\
├── Vendor Performance Analysis         # Pyhon-based Vendor performance specific analysis\
├── Dashboard.pbix                      # Power BI file
├── logs/                               # Ingestion logs\
├── data/                               # Raw CSV data (Sample)\
└── README.md                           # Project documentation\

# Tech Stack
| Category             | Tools Used                                         |
|----------------------|----------------------------------------------------|
| Programming & Analysis | Python (Pandas, NumPy, Seaborn, Matplotlib)      |
| Database             | SQLite via SQLAlchemy                              |
| Visualization        | Power BI                                           |
| Scripting            | Python-based data ingestion                        |
| Statistical Testing  | Confidence intervals, t-tests                      |


# Analytical Workflow
## Python Phase
1. *Data Ingestion:* Using SQLAlchemy and pandas to store CSVs in SQLite.
2. *Data Cleaning:* Filtering invalid rows (zero sales, negative profits).
3. *EDA:* Summary stats, correlations, and outlier detection.
4. *Analysis:*
    * Profitability comparison across vendors.
    * Statistical tests (t-test, confidence intervals).
    * Bulk purchase cost savings.
    * Unsold inventory valuation.
## Power BI Phase
1. *Python Data Connection:* Used Python script to import the cleaned dataset from SQLite.
2. *Transformations:* Applied Power Query filters to refine vendor summary data.
3. *DAX Calculations:* Created calculated tables, columns, and measures for KPIs.
4. *Dashboard Design*\
Each visual ties back to analytical findings derived in Python, providing a real-time, interactive representation of vendor performance.
<img width="1295" height="730" alt="Screenshot Dashboard" src="https://github.com/user-attachments/assets/39d1efba-b8ac-4bf4-b6a3-18ccf52454ae" />

