import sqlite3
import pandas as pd

DB_PATH = "database/medsupply.db"
conn = sqlite3.connect(DB_PATH)

print("\nConnected to DB:", DB_PATH)

def run(query: str, title: str, n=10):
    print("\n" + "="*90)
    print(title)
    print("="*90)
    df = pd.read_sql(query, conn)
    print(df.head(n))
    print("Rows:", len(df))
    return df

# 1) Total units by product
run("""
SELECT product, ROUND(SUM(units_sold), 2) AS total_units
FROM sales
GROUP BY product
ORDER BY total_units DESC;
""", "1) Total units by product")

# 2) Monthly demand by product
run("""
SELECT strftime('%Y-%m', date) AS year_month,
       product,
       ROUND(SUM(units_sold), 2) AS monthly_units
FROM sales
GROUP BY year_month, product
ORDER BY year_month, monthly_units DESC;
""", "2) Monthly demand by product")

# 3) Weekday demand pattern
run("""
SELECT "Weekday Name" AS weekday,
       product,
       ROUND(AVG(units_sold), 2) AS avg_units
FROM sales
GROUP BY weekday, product
ORDER BY avg_units DESC;
""", "3) Average daily demand by weekday")

# 4) NULL handling demonstration using COALESCE
# (Your cleaned data likely has no NULLs, but this shows you know how to handle them.)
run("""
SELECT product,
       ROUND(SUM(COALESCE(units_sold, 0)), 2) AS total_units_safe
FROM sales
GROUP BY product
ORDER BY total_units_safe DESC;
""", "4) NULL handling with COALESCE")

# 5) CASE WHEN: Demand bucket by daily units
run("""
SELECT date,
       product,
       units_sold,
       CASE
         WHEN units_sold >= 50 THEN 'HIGH'
         WHEN units_sold >= 20 THEN 'MEDIUM'
         ELSE 'LOW'
       END AS demand_bucket
FROM sales
ORDER BY units_sold DESC
LIMIT 50;
""", "5) CASE WHEN: bucket high/medium/low demand days", n=20)

# 6) Window function: 7-day moving average (ma7)
try:
    run("""
    SELECT date,
           product,
           units_sold,
           ROUND(AVG(units_sold) OVER (
               PARTITION BY product
               ORDER BY date
               ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           ), 2) AS ma7
    FROM sales
    ORDER BY product, date;
    """, "6) Window function: 7-day moving average", n=10)
except Exception as e:
    print("\n❌ Window function not supported in your SQLite build.")
    print("Error:", e)
    print("We’ll compute moving averages in pandas later (still OK for interview).")

# 7) LAG: Day-over-day change (another window function)
try:
    run("""
    SELECT date,
           product,
           units_sold,
           LAG(units_sold) OVER (PARTITION BY product ORDER BY date) AS prev_day_units,
           ROUND(
             units_sold - LAG(units_sold) OVER (PARTITION BY product ORDER BY date),
             2
           ) AS day_change
    FROM sales
    ORDER BY product, date;
    """, "7) Window function: LAG for day-over-day change", n=10)
except Exception as e:
    print("\n❌ LAG window function not supported.")
    print("Error:", e)

# 8) Spike detection: days where units_sold is > 3x product average
run("""
WITH avg_units AS (
  SELECT product, AVG(units_sold) AS avg_u
  FROM sales
  GROUP BY product
)
SELECT s.date, s.product, s.units_sold, ROUND(a.avg_u, 2) AS avg_units,
       ROUND(s.units_sold / a.avg_u, 2) AS multiple_of_avg
FROM sales s
JOIN avg_units a ON s.product = a.product
WHERE s.units_sold > 3 * a.avg_u
ORDER BY multiple_of_avg DESC;
""", "8) Spike detection (JOIN): days > 3x product average", n=20)

conn.close()
print("\n✅ Done.")
