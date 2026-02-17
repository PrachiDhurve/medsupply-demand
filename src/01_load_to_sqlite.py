import os
import sqlite3
import pandas as pd

CSV_PATH = os.path.join("data", "salesdaily.csv")     #this means the path is data/salesdaily.csv
DB_PATH = os.path.join("database", "medsupply.db")    # path going to be database/medsupply.db

def main():
    # 1) Read CSV
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Could not find {CSV_PATH}. Make sure salesdaily.csv is inside /data folder.")

    df = pd.read_csv(CSV_PATH)     #creates dataframe, now CSV is in memory(df)

    print("✅ Loaded CSV:", CSV_PATH)
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("\nSample rows:")
    print(df.head(3))

    # 2) Create SQLite DB + store raw table
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)       # will create a databse folder (database is the folder given in DB_PATH) - if already exists no error 
    
    #connect to sqlite
    conn = sqlite3.connect(DB_PATH)                                 
    #save dataframe to db
    df.to_sql("raw_daily", conn, if_exists="replace", index=False)   #it  creates table raw_daily

    conn.close()
    print(f"\n✅ Saved table raw_daily into SQLite DB: {DB_PATH}")

if __name__ == "__main__":
    main()
