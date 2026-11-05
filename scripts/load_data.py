import os
import pandas as pd
import mysql.connector

df = pd.read_csv("SFILS_EXCELSHEET.csv", encoding="utf-8-sig")

df.columns = [str(c).split("\n")[0].strip() for c in df.columns]
print(df.columns.tolist())

for col in ["Provided Email Address", "Within San Francisco County"]:
    df[col] = df[col].map({True: 1, False: 0, "True": 1, "False": 0})

df = df.astype(object).where(df.notna(), None)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ["SQL_PASSWORD"],
    database="sfils2026",
)
cur = conn.cursor()

def load_lookup(table, code_col, def_col):
    pairs = df.groupby(code_col)[def_col].first().reset_index().fillna("Unknown")
    cur.executemany(f"INSERT IGNORE INTO {table} VALUES (%s, %s)", pairs.values.tolist())

load_lookup("patron_types", "Patron Type Code", "Patron Type Definition")
load_lookup("home_libraries", "Home Library Code", "Home Library Definition")
load_lookup("notification_types", "Notification Preference Code", "Notification Code Definition")

def check(col, table, key):
    cur.execute(f"SELECT {key} FROM {table}")
    known = {r[0] for r in cur.fetchall()}
    bad = df[df[col].notna() & ~df[col].isin(known)][col].unique()
    print(col, "-> missing from", table, ":", bad)

check("Patron Type Code", "patron_types", "patron_type_code")
check("Home Library Code", "home_libraries", "home_library_code")
check("Notification Preference Code", "notification_types", "notification_medium_code")

cols = ["Patron Type Code", "Total Checkouts", "Total Renewals", "Age Range",
        "Home Library Code", "Circulation Active Month",
        "Circulation Active Year", "Notification Preference Code",
        "Provided Email Address", "Within San Francisco County",
        "Year Patron Registered"]

cur.executemany(
    """INSERT INTO patrons
       (patron_type_code, total_checkouts, total_renewals, age_range,
        home_library_code, circulation_active_month, circulation_active_year,
        notification_medium_code, provided_email_address, within_sf_county, year_patron_registered)
       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
    df[cols].values.tolist(),
)

conn.commit()
print("Loaded", len(df), "rows")
cur.close()
conn.close()