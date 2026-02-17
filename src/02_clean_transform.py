import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("database", "medsupply.db")

def main():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Database not found. Run src/01_load_to_sqlite.py first.")

    #opens connection so we can read/write tabels.
    conn = sqlite3.connect(DB_PATH)

    # Read raw table
    df = pd.read_sql("SELECT * FROM raw_daily", conn)

    # Rename date column
    df = df.rename(columns={"datum": "date"})

    # Convert date
    df["date"] = pd.to_datetime(df["date"])

    # Product columns (drug codes)
    product_cols = ["M01AB", "M01AE", "N02BA", "N02BE", "N05B", "N05C", "R03", "R06"]

    # Convert wide -> long
    df_long = df.melt(                        # melt transforms wide format to long format
        id_vars=["date", "Year", "Month", "Weekday Name"],
        value_vars=product_cols,               # value_vars tells pandas which columns to unpivot(covert to rows)
        var_name="product",                    # creates new column product (it has column names from value_vars)
        value_name="units_sold"                # creates new column units_sold (it has actual numbers inside the cells)
    )

    # Convert units to numeric safely
    df_long["units_sold"] = pd.to_numeric(df_long["units_sold"], errors="coerce")

    # Remove NULL/0 sales
    df_long = df_long.dropna(subset=["units_sold"])
    df_long = df_long[df_long["units_sold"] > 0]

    # Save cleaned table
    df_long.to_sql("sales", conn, if_exists="replace", index=False)

    # Quick check
    print("✅ Created clean table: sales")
    print("Rows:", len(df_long))
    print(df_long.head(10))

    conn.close()

if __name__ == "__main__":
    main()
