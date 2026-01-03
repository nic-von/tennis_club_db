import sqlite3
import os
from datetime import datetime

DB_NAME = "tennisclub.db"

def get_connection():
    if not os.path.exists(DB_NAME):
        print(f"[WARNING] Η βάση {DB_NAME} δεν βρέθηκε! Δημιουργείται νέα.")
    
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON;") 
    return con

# --- Γενικές Συναρτήσεις ---
def get_table_names():
    con = get_connection()
    try:
        cursor = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row['name'] for row in cursor.fetchall() if row['name'] != 'sqlite_sequence']
        return tables
    finally:
        con.close()

def select_table(table_name):
    allowed = get_table_names()
    if table_name not in allowed:
        raise ValueError("Μη έγκυρο όνομα πίνακα.")
    
    con = get_connection()
    try:
        cursor = con.execute(f"SELECT * FROM {table_name}")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        con.close()

# ======================= MEMBER MANAGEMENT =======================

def create_member(first_name, last_name, phone, mail, address, dob):
    con = get_connection()
    try:
        cur = con.execute("""
            INSERT INTO Member (first_name, last_name, phone, mail, address, date_of_birth)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, phone, mail, address, dob))
        con.commit()
        return cur.lastrowid
    finally:
        con.close()

def get_member(member_id):
    con = get_connection()
    try:
        cur = con.execute("SELECT * FROM Member WHERE member_id = ?", (member_id,))
        row = cur.fetchone()
        if not row: raise LookupError("Το μέλος δεν βρέθηκε.")
        return dict(row)
    finally:
        con.close()

def update_member_field(member_id, field, value):
    allowed_fields = {'first_name', 'last_name', 'phone', 'mail', 'address', 'date_of_birth'}
    if field not in allowed_fields:
        raise ValueError(f"Μη επιτρεπτό πεδίο: {field}")
    
    con = get_connection()
    try:
        query = f"UPDATE Member SET {field} = ? WHERE member_id = ?"
        cur = con.execute(query, (value, member_id))
        con.commit()
        if cur.rowcount == 0: raise LookupError("Το μέλος δεν βρέθηκε.")
    finally:
        con.close()

# ======================= COURTS & RESERVATIONS (NEW) =======================

def create_court(court_type, comments=""):
    con = get_connection()
    try:
        con.execute("INSERT INTO Court (type, comments) VALUES (?, ?)", (court_type, comments))
        con.commit()
    finally:
        con.close()

def schedule_maintenance(court_id, description, start, end):
    con = get_connection()
    try:
        con.execute("""
            INSERT INTO Maintenance (court_id, description, start_datetime, end_datetime)
            VALUES (?, ?, ?, ?)
        """, (court_id, description, start, end))
        con.commit()
    finally:
        con.close()

def create_reservation(member_id, court_id, date, start_time, end_time, num_people, cost=20):
    """Δημιουργεί κράτηση (Πληρωμή -> Κράτηση). Transactional."""
    con = get_connection()
    try:
        cur = con.cursor()
        # 1. Πληρωμή
        cur.execute("INSERT INTO Payment (amount, payment_method, member_id) VALUES (?, 'Card', ?)", 
                    (cost, member_id))
        payment_id = cur.lastrowid

        # 2. Κράτηση
        cur.execute("""
            INSERT INTO Reservation (date, start_time, end_time, num_of_people, cost, member_id, court_id, payment_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (date, start_time, end_time, num_people, cost, member_id, court_id, payment_id))
        
        con.commit()
        return cur.lastrowid
    except Exception as e:
        con.rollback()
        raise e
    finally:
        con.close()

def get_member_reservations(member_id):
    """Επιστρέφει τις μελλοντικές κρατήσεις ενός μέλους."""
    sql = """
        SELECT reservation_id, date, start_time, end_time, court_id, cost 
        FROM Reservation 
        WHERE member_id = ? AND date >= date('now')
        ORDER BY date, start_time
    """
    con = get_connection()
    try:
        cur = con.execute(sql, (member_id,))
        return [dict(row) for row in cur.fetchall()]
    finally:
        con.close()

def update_reservation(reservation_id, new_date, new_start, new_end):
    """Τροποποίηση κράτησης."""
    con = get_connection()
    try:
        cur = con.execute("""
            UPDATE Reservation 
            SET date = ?, start_time = ?, end_time = ? 
            WHERE reservation_id = ?
        """, (new_date, new_start, new_end, reservation_id))
        con.commit()
        if cur.rowcount == 0: raise LookupError("Η κράτηση δεν βρέθηκε.")
    finally:
        con.close()

# ======================= TOURNAMENTS (NEW) =======================

def create_tournament(name, category, start, end):
    con = get_connection()
    try:
        con.execute("""
            INSERT INTO Tournament (name, category, start_date, end_date)
            VALUES (?, ?, ?, ?)
        """, (name, category, start, end))
        con.commit()
    finally:
        con.close()

def get_upcoming_tournaments():
    con = get_connection()
    try:
        cur = con.execute("SELECT * FROM Tournament WHERE start_date >= date('now')")
        return [dict(row) for row in cur.fetchall()]
    finally:
        con.close()

def register_member_to_tournament(member_id, tournament_id, cost=50):
    """Εγγραφή σε τουρνουά (Πληρωμή -> Tournament_fee). Transactional."""
    con = get_connection()
    try:
        cur = con.cursor()
        # 1. Πληρωμή
        cur.execute("INSERT INTO Payment (amount, payment_method, member_id) VALUES (?, 'Online', ?)", 
                    (cost, member_id))
        payment_id = cur.lastrowid

        # 2. Εγγραφή (Tournament_fee)
        signup_date = datetime.now().strftime("%Y-%m-%d")
        cur.execute("""
            INSERT INTO Tournament_fee (member_id, tournament_id, payment_id, cost, sign_up_date)
            VALUES (?, ?, ?, ?, ?)
        """, (member_id, tournament_id, payment_id, cost, signup_date))
        
        con.commit()
    except Exception as e:
        con.rollback()
        raise e
    finally:
        con.close()

def create_match(tournament_id, court_id, member1, member2, start, end, phase="Group Stage"):
    con = get_connection()
    try:
        con.execute("""
            INSERT INTO Match (tournament_id, court_id, member1_id, member2_id, start_datetime, end_datetime, phase)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tournament_id, court_id, member1, member2, start, end, phase))
        con.commit()
    finally:
        con.close()

def record_match_result(match_id, score, winner_id, comment=""):
    con = get_connection()
    try:
        cur = con.execute("""
            UPDATE Match SET score = ?, winner_id = ?, comment = ? WHERE match_id = ?
        """, (score, winner_id, comment, match_id))
        con.commit()
        if cur.rowcount == 0: raise LookupError("Ο αγώνας δεν βρέθηκε.")
    finally:
        con.close()

# ======================= SCHEDULE & STATS =======================

def get_filtered_schedule(court_id=None, date=None):
    sql = "SELECT * FROM Global_Court_Schedule WHERE 1=1"
    params = []
    if court_id:
        sql += " AND court_id = ?"
        params.append(court_id)
    if date:
        sql += " AND start_datetime LIKE ?"
        params.append(f"{date}%")
    sql += " ORDER BY start_datetime ASC"

    con = get_connection()
    try:
        cursor = con.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        con.close()

def get_financial_stats():
    con = get_connection()
    try:
        stats = {}
        cur = con.execute("SELECT COUNT(*) as count FROM Member")
        res = cur.fetchone()
        stats['total_members'] = res['count'] if res else 0
        
        cur = con.execute("SELECT SUM(amount) as total FROM Payment")
        res = cur.fetchone()
        stats['total_revenue'] = res['total'] if res and res['total'] else 0.0
        return stats
    finally:
        con.close()

def get_member_stats():
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
    con = get_connection()
    try:
        cursor = con.execute(sql)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        con.close()

# ======================= LESSONS =======================

def get_lesson_availability():
    sql = """
    SELECT l.lesson_id, l.level, l.start_datetime, l.max_capacity, 
           COUNT(scl.payment_id) AS enrolled,
           (l.max_capacity - COUNT(scl.payment_id)) AS remaining
    FROM Lesson l
    LEFT JOIN Subscription_concerning_Lesson scl ON l.lesson_id = scl.lesson_id
    GROUP BY l.lesson_id;
    """
    con = get_connection()
    try:
        cursor = con.execute(sql)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        con.close()

def enroll_member_in_lesson(member_id, lesson_id, discount, amount, payment_method):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO Payment (discount, payment_method, member_id) VALUES (?, ?, ?)", 
                    (discount, payment_method, member_id))
        if discount=='1':
            discount = 0.5
        else: discount = 1
        payment_id = cur.lastrowid
        cur.execute("INSERT INTO Subscription (payment_id, cost) VALUES (?, ?)", 
                    (payment_id, amount))
        cur.execute("INSERT INTO Subscription_concerning_Lesson (payment_id, lesson_id) VALUES (?, ?)", 
                    (payment_id, lesson_id))
        con.commit()
    except Exception as e:
        con.rollback()
        raise e
    finally:
        con.close()

def delete_orphan_payments():
    sql = """
    DELETE FROM Payment
    WHERE payment_id NOT IN (SELECT payment_id FROM Reservation)
      AND payment_id NOT IN (SELECT payment_id FROM Subscription)
      AND payment_id NOT IN (SELECT payment_id FROM Tournament_fee);
    """
    con = get_connection()
    try:
        cur = con.execute(sql)
        con.commit()
        return cur.rowcount
    finally:
        con.close()