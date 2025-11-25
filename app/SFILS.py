import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",      
        user="root",           
        password="josh2004",  
        database="sfils_db"    
    )

def checkout_total_overall():
    con = get_connection()
    cur = con.cursor()

    query = """
        SELECT SUM(checkout_total) AS overall_total
        FROM circulation;
    """

    cur.execute(query)
    result = cur.fetchone()

    if result and result[0]:
        total = result[0]
    else:
        total = 0
    print("Overall Checkout Total: ", total)

    cur.close()
    con.close()

def most_active_patron():
    con = get_connection()
    cur = con.cursor()

    query = """
        SELECT 
	        p.patron_id,
            p.patron_type_definition,
            SUM(c.checkout_total) AS overall_total
        FROM patrons p
        JOIN circulation c ON p.patron_id = c.patron_id
        GROUP BY p.patron_id, p.patron_type_definition
        ORDER BY overall_total DESC
        LIMIT 1;
    """

    cur.execute(query)
    row = cur.fetchone()

    if row: 
        id, type, total = row
        print("Most Active Patron: ID {id} ({type}) total checkout = {total}")
    else:
        print("Data Unavailable")
        

    cur.close()
    con.close()

if __name__ == "__main__":

    checkout_total_overall()
    most_active_patron()



