import sqlite3
import pandas as pd
import logging
import os
from ingestion_db import ingest_db

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Reset existing handlers (important in Jupyter or repeated runs)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s", 
    filemode="a"
)

def create_vendor_summary(conn):
    '''this function will merge the diffferent tables to get the overall vendor summary and adding new columns in the resultant table'''
    vendor_sales_summary = pd.read_sql_query("""WITH FreightSummary as (
            select VendorNumber, sum(Freight) as FreightCost 
            from vendor_invoice 
            group by VendorNumber),
            
            PurchaseSummary as (
            SELECT p.VendorNumber, p.VendorName, p.Brand, p.Description,
            p.PurchasePrice, pp.Price as ActualPrice, pp.Volume,
            SUM(p.Quantity) as TotalPurchaseQuantity, 
            SUM(p.Dollars) as TotalPurchaseDollars 
            FROM purchases p
            JOIN purchase_prices pp 
                ON p.Brand = pp.Brand
            WHERE p.PurchasePrice > 0
            GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume),
            
            SalesSummary as (
            SELECT VendorNo, Brand,
            SUM(SalesDollars) as TotalSalesDollars, 
            SUM(SalesPrice) as TotalSalesPrice, 
            SUM(SalesQuantity) as TotalSalesQuantity,
            SUM(ExciseTax) as TotalExciseTax
            FROM sales
            GROUP BY VendorNo, Brand)
            
            Select
            ps.VendorNumber, ps.VendorName, ps.Brand, ps.Description,
            ps.PurchasePrice, ps.ActualPrice, ps.Volume,
            ps.TotalPurchaseQuantity, ps.TotalPurchaseDollars,
            ss.TotalSalesQuantity, ss.TotalSalesDollars, ss.TotalSalesPrice, ss.TotalExciseTax, 
            fs.FreightCost 
            FROM PurchaseSummary ps
            LEFT JOIN SalesSummary ss
                ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
            LEFT JOIN FreightSummary fs
                ON ps.VendorNumber = fs.VendorNumber 
            ORDER BY ps.TotalPurchaseDollars DESC""", conn)
    return vendor_sales_summary

def clean_data(df):
    '''This function will help clean data - fill misiing values, ensure correct data types, remove extra spaces in strings and add new columns'''
    # Change datatype to float
    df['Volume'] = df['Volume'].astype('float64')

    # Fill missing values with 0
    df.fillna(0, inplace = True)

    # Remove space from Categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    # Create additional required columns for better analysis
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars'])*100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalesToPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']

    return df

if __name__ == '__main__':
    #creating database connection
    conn = sqlite3.connect("inventory.db")

    logging.info("Creating Vendor Summary Table.....")
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())

    logging.info('Cleaning Data.....')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting data into database.....')
    ingest_db(clean_df, 'vendor_sales_summary', conn)
    logging.info('Ingestion Complete!')

