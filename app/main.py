import os
import pandas as pd
import mysql.connector

def run(query):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ["SQL_PASSWORD"],
        database="sfils2026",
    )
    cur = conn.cursor()
    cur.execute(query)
    df = pd.DataFrame(cur.fetchall(), columns=cur.column_names)
    cur.close()
    conn.close()
    return df

def repeat_patrons():
    return run("""
        SELECT COUNT(*) AS total_patrons,
            SUM(total_checkouts > 1) AS repeat_patrons,
            ROUND(100 * SUM(total_checkouts > 1) / COUNT(*), 1) AS repeat_pct
        FROM patrons
    """)

def renewals():
    return run("""
        SELECT SUM(total_renewals > 0) AS patrons_who_renewed,
            SUM(total_renewals) AS total_renewals,
            ROUND(100 * SUM(total_renewals > 0) / COUNT(*), 1) AS renewed_pct
        FROM patrons
    """)

def most_active_patron():
    return run("""
        SELECT p.total_checkouts,
            p.total_renewals,
            p.age_range,
            t.patron_type_definition,
            h.home_library_definition,
            p.year_patron_registered
        FROM patrons p
        LEFT JOIN patron_types t ON p.patron_type_code = t.patron_type_code
        LEFT JOIN home_libraries h ON p.home_library_code = h.home_library_code
        WHERE p.total_checkouts = (SELECT MAX(total_checkouts) FROM patrons)
    """)


if __name__ == "__main__":
    print(repeat_patrons(), "\n")
    print(renewals(), "\n")
    print(most_active_patron())
