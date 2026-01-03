import sqlite3

DB_NAME = "tennisclub.db"

def get_connection():
    con = sqlite3.connect(DB_NAME)
    con.execute("PRAGMA foreign_keys = ON;") 
    return con

# --- Γενικές Συναρτήσεις ---
def get_table_names():
    with get_connection() as con:
        cursor = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']
    return tables

def select_table(table_name):
    with get_connection() as con:
        # Προσοχή: Χρήση μόνο για tables που ελέγξαμε ότι υπάρχουν (όχι user input)
        cursor = con.execute(f"SELECT * FROM {table_name}")
        colnames = [d[0] for d in cursor.description]
        return [dict(zip(colnames, row)) for row in cursor.fetchall()]

# --- Ειδικές Λειτουργίες (Business Logic) ---

def get_lesson_availability():
    """Query 1: Διαθεσιμότητα Θέσεων σε Μαθήματα"""
    sql = """
    SELECT l.lesson_id, l.level, l.max_capacity, 
           COUNT(scl.payment_id) AS enrolled_students,
           (l.max_capacity - COUNT(scl.payment_id)) AS remaining_spots
    FROM Lesson l
    LEFT JOIN Subscription_concerning_Lesson scl ON l.lesson_id = scl.lesson_id
    GROUP BY l.lesson_id;
    """
    with get_connection() as con:
        cursor = con.execute(sql)
        colnames = [d[0] for d in cursor.description]
        return [dict(zip(colnames, row)) for row in cursor.fetchall()]

def get_member_stats():
    """Query 8: Στατιστικά Μελών & Status (VIP, Pro, etc.)"""
    sql = """
    SELECT m.first_name || ' ' || m.last_name AS Full_Name,
        COUNT(DISTINCT r.payment_id) AS Total_Reservations,
        COUNT(DISTINCT scl.lesson_id) AS Total_Lessons_Enrolled,
        CASE 
            WHEN COUNT(DISTINCT r.payment_id) > 5 THEN 'VIP Player'
            WHEN COUNT(DISTINCT tf.tournament_id) > 0 AND COUNT(DISTINCT scl.lesson_id) > 0 THEN 'Pro Student'
            WHEN COUNT(DISTINCT scl.lesson_id) > 0 THEN 'Active Student'
            ELSE 'Casual Player'
        END AS Member_Status
    FROM Member m
    LEFT JOIN Payment p ON m.member_id = p.member_id
    LEFT JOIN Subscription s ON p.payment_id = s.payment_id
    LEFT JOIN Subscription_concerning_Lesson scl ON s.payment_id = scl.payment_id
    LEFT JOIN Tournament_fee tf ON p.payment_id = tf.payment_id
    LEFT JOIN Reservation r ON p.payment_id = r.payment_id
    GROUP BY m.member_id
    ORDER BY Total_Reservations DESC;
    """
    with get_connection() as con:
        cursor = con.execute(sql)
        colnames = [d[0] for d in cursor.description]
        return [dict(zip(colnames, row)) for row in cursor.fetchall()]

def enroll_member_in_lesson(member_id, lesson_id, amount, payment_method="Cash"):
    """Query 7: Εγγραφή Μέλους σε Μάθημα (Transaction)"""
    # Αυτή η ενέργεια απαιτεί 3 βήματα. Αν αποτύχει το ένα, πρέπει να ακυρωθούν όλα.
    con = get_connection()
    try:
        cur = con.cursor()
        
        # 1. Καταγραφή Πληρωμής
        cur.execute("""
            INSERT INTO Payment (amount, payment_method, member_id) 
            VALUES (?, ?, ?);
        """, (amount, payment_method, member_id))
        payment_id = cur.lastrowid
        
        # 2. Δημιουργία Συνδρομής
        cur.execute("""
            INSERT INTO Subscription (payment_id, cost, member_id, lesson_id) 
            VALUES (?, ?, ?, ?);
        """, (payment_id, amount, member_id, lesson_id))
        
        # 3. Σύνδεση Συνδρομής με Μάθημα
        cur.execute("""
            INSERT INTO Subscription_concerning_Lesson (payment_id, lesson_id) 
            VALUES (?, ?);
        """, (payment_id, lesson_id))
        
        con.commit() # Οριστικοποίηση αλλαγών
        return True
    except Exception as e:
        con.rollback() # Ακύρωση αν κάτι πάει στραβά
        raise e
    finally:
        con.close()

def delete_orphan_payments():
    """Query 2: Καθαρισμός Ορφανών Πληρωμών"""
    sql = """
    DELETE FROM Payment
    WHERE payment_id NOT IN (SELECT payment_id FROM Reservation)
      AND payment_id NOT IN (SELECT payment_id FROM Subscription)
      AND payment_id NOT IN (SELECT payment_id FROM Tournament_fee);
    """
    with get_connection() as con:
        cur = con.execute(sql)
        con.commit()
        return cur.rowcount