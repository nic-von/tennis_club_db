import sqlite3

DB_NAME = "tennisclub.db"

def get_connection():
    con = sqlite3.connect(DB_NAME)
    con.execute("PRAGMA foreign_keys = ON;") 
    return con
# ======================= MEMBER OPERATIONS =======================

def insert_member(first_name, last_name, phone, mail, address, date_of_birth):
    """Εισάγει ένα νέο μέλος στη βάση δεδομένων"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute(
            "INSERT INTO Member (first_name, last_name, phone, mail, address, date_of_birth) VALUES (?, ?, ?, ?, ?, ?)",
            (first_name, last_name, phone, mail, address, date_of_birth)
        )
        con.commit()
        member_id = cursor.lastrowid
        con.close()
        
        return {"success": True, "member_id": member_id}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

def get_member_by_id(member_id):
    """Λαμβάνει τα στοιχεία ενός μέλους από το ID του"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute(
            "SELECT member_id, first_name, last_name, phone, mail, address, date_of_birth FROM Member WHERE member_id = ?",
            (member_id,)
        )
        member = cursor.fetchone()
        con.close()
        
        return member
    
    except sqlite3.Error as e:
        return None

def update_member(member_id, field, value):
    """Ενημερώνει ένα πεδίο ενός μέλους"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        # Έλεγχος ότι το πεδίο είναι έγκυρο
        valid_fields = ["first_name", "last_name", "phone", "mail", "address", "date_of_birth"]
        if field not in valid_fields:
            return {"success": False, "error": "Μη έγκυρο πεδίο"}
        
        query = f"UPDATE Member SET {field} = ? WHERE member_id = ?"
        cursor.execute(query, (value, member_id))
        con.commit()
        con.close()
        
        return {"success": True}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

# ======================= STATISTICS =======================

def get_stats():
    """Λαμβάνει στατιστικά για το σύστημα"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        # Συνολικά μέλη
        cursor.execute("SELECT COUNT(*) FROM Member")
        total_members = cursor.fetchone()[0]
        
        # Συνολικές πληρωμές
        cursor.execute("SELECT COALESCE(SUM(cost), 0) FROM Payment")
        total_payments = cursor.fetchone()[0]
        
        con.close()
        
        return {
            "total_members": total_members,
            "total_payments": total_payments
        }
    
    except sqlite3.Error as e:
        return {"error": f"Σφάλμα: {e}"}

# ======================= PROGRAM =======================

def get_future_program(start_date=None, court_id=None, activity_type=None):
    """Λαμβάνει το μελλοντικό πρόγραμμα γηπέδων (χρησιμοποιεί το Global_Court_Schedule VIEW)
    
    Args:
        start_date: Ημερομηνία έναρξης (YYYY-MM-DD) ή None για όλο
        court_id: ID γηπέδου ή None για όλα
        activity_type: Τύπος δραστηριότητας ('Lesson', 'Maintenance', 'Match', 'Reservation') ή None για όλα
    
    Returns:
        Λίστα με τα αποτελέσματα
    """
    try:
        con = get_connection()
        cursor = con.cursor()
        
        # Δημιουργία WHERE clause
        where_conditions = ["datetime(start_datetime) > datetime('now')"]
        params = []
        
        if start_date is not None:
            where_conditions[0] = "datetime(start_datetime) >= datetime(?)"
            params.append(start_date)
        
        if court_id is not None:
            where_conditions.append("court_id = ?")
            params.append(court_id)
        
        if activity_type is not None:
            where_conditions.append("activity = ?")
            params.append(activity_type)
        
        where_clause = " AND ".join(where_conditions)
        
        query = f"""
            SELECT * FROM Global_Court_Schedule 
            WHERE {where_clause}
            ORDER BY start_datetime
        """
        
        if params:
            cursor.execute(query, tuple(params))
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        con.close()
        
        return results if results else None
    
    except sqlite3.Error as e:
        return None

# ======================= COURT OPERATIONS =======================

def get_all_courts():
    """Λαμβάνει όλα τα γήπεδα από τη βάση δεδομένων"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute("SELECT court_id, Type, comments FROM Court ORDER BY court_id")
        courts = cursor.fetchall()
        con.close()
        
        return courts
    
    except sqlite3.Error as e:
        return None

def insert_court(court_type, comments=None):
    """Εισάγει ένα νέο γήπεδο στη βάση δεδομένων"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute(
            "INSERT INTO Court (Type, comments) VALUES (?, ?)",
            (court_type, comments)
        )
        con.commit()
        court_id = cursor.lastrowid
        con.close()
        
        return {"success": True, "court_id": court_id}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

def get_court_by_id(court_id):
    """Λαμβάνει τα στοιχεία ενός γηπέδου από το ID του"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute(
            "SELECT court_id, Type, comments FROM Court WHERE court_id = ?",
            (court_id,)
        )
        court = cursor.fetchone()
        con.close()
        
        return court
    
    except sqlite3.Error as e:
        return None

def update_court(court_id, field, value):
    """Ενημερώνει ένα πεδίο ενός γηπέδου"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        # Έλεγχος ότι το πεδίο είναι έγκυρο
        valid_fields = ["Type", "comments"]
        if field not in valid_fields:
            return {"success": False, "error": "Μη έγκυρο πεδίο"}
        
        query = f"UPDATE Court SET {field} = ? WHERE court_id = ?"
        cursor.execute(query, (value, court_id))
        con.commit()
        con.close()
        
        return {"success": True}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

def delete_court(court_id):
    """Διαγράφει ένα γήπεδο από τη βάση δεδομένων"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        # Διαγραφή γηπέδου
        cursor.execute("DELETE FROM Court WHERE court_id = ?", (court_id,))
        
        # Ενημέρωση του sqlite_sequence για να επανέλθει στο τελευταίο ID
        cursor.execute("SELECT MAX(court_id) FROM Court")
        max_id = cursor.fetchone()[0]
        
        if max_id is not None:
            cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'Court'", (max_id,))
        else:
            # Αν δεν υπάρχουν γήπεδα, θέτουμε seq = 0
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'Court'")
        
        con.commit()
        con.close()
        
        return {"success": True}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

def insert_maintenance(court_id, start_datetime, description=None):
    """Εισάγει συντήρηση στη βάση δεδομένων (end_datetime = NULL)"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute(
            "INSERT INTO Maintenance (court_id, start_datetime, end_datetime, description) VALUES (?, ?, NULL, ?)",
            (court_id, start_datetime, description)
        )
        con.commit()
        maintenance_id = cursor.lastrowid
        con.close()
        
        return {"success": True, "maintenance_id": maintenance_id}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

def get_maintenance_by_id(maintenance_id):
    """Λαμβάνει τα στοιχεία μιας συντήρησης από το ID της"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute(
            "SELECT maintenance_id, court_id, start_datetime, end_datetime, description FROM Maintenance WHERE maintenance_id = ?",
            (maintenance_id,)
        )
        maintenance = cursor.fetchone()
        con.close()
        
        return maintenance
    
    except sqlite3.Error as e:
        return None

def update_maintenance(maintenance_id, field, value):
    """Ενημερώνει ένα πεδίο μιας συντήρησης"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        # Έλεγχος ότι το πεδίο είναι έγκυρο
        valid_fields = ["court_id", "start_datetime", "end_datetime", "description"]
        if field not in valid_fields:
            return {"success": False, "error": "Μη έγκυρο πεδίο"}
        
        # Αν το value είναι κενό string για end_datetime, θέστε το ως NULL
        if field == "end_datetime" and value == "":
            value = None
        
        query = f"UPDATE Maintenance SET {field} = ? WHERE maintenance_id = ?"
        cursor.execute(query, (value, maintenance_id))
        con.commit()
        con.close()
        
        return {"success": True}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

def delete_maintenance(maintenance_id):
    """Διαγράφει μια συντήρηση από τη βάση δεδομένων"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        # Διαγραφή συντήρησης
        cursor.execute("DELETE FROM Maintenance WHERE maintenance_id = ?", (maintenance_id,))
        
        # Ενημέρωση του sqlite_sequence για να επανέλθει στο τελευταίο ID
        cursor.execute("SELECT MAX(maintenance_id) FROM Maintenance")
        max_id = cursor.fetchone()[0]
        
        if max_id is not None:
            cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'Maintenance'", (max_id,))
        else:
            # Αν δεν υπάρχουν συντηρήσεις, θέτουμε seq = 0
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'Maintenance'")
        
        con.commit()
        con.close()
        
        return {"success": True}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

# ======================= TOURNAMENT OPERATIONS =======================

def get_all_tournaments():
    """Λαμβάνει όλα τα τουρνουά από τη βάση δεδομένων"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute("""
            SELECT tournament_id, name, category, start_date, end_date 
            FROM Tournament 
            ORDER BY start_date DESC
        """)
        tournaments = cursor.fetchall()
        con.close()
        
        return tournaments if tournaments else None
    
    except sqlite3.Error as e:
        return None

def get_tournament_by_id(tournament_id):
    """Λαμβάνει τα στοιχεία ενός τουρνουά από το ID του"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute(
            "SELECT tournament_id, name, category, start_date, end_date FROM Tournament WHERE tournament_id = ?",
            (tournament_id,)
        )
        tournament = cursor.fetchone()
        con.close()
        
        return tournament
    
    except sqlite3.Error as e:
        return None

def insert_tournament(name, category, start_date, end_date):
    """Εισάγει ένα νέο τουρνουά στη βάση δεδομένων"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute(
            "INSERT INTO Tournament (name, category, start_date, end_date) VALUES (?, ?, ?, ?)",
            (name, category, start_date, end_date)
        )
        con.commit()
        tournament_id = cursor.lastrowid
        con.close()
        
        return {"success": True, "tournament_id": tournament_id}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

def update_tournament(tournament_id, field, value):
    """Ενημερώνει ένα πεδίο ενός τουρνουά"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        valid_fields = ["name", "category", "start_date", "end_date"]
        if field not in valid_fields:
            return {"success": False, "error": "Μη έγκυρο πεδίο!"}
        
        query = f"UPDATE Tournament SET {field} = ? WHERE tournament_id = ?"
        cursor.execute(query, (value, tournament_id))
        con.commit()
        con.close()
        
        return {"success": True}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

def delete_tournament(tournament_id):
    """Διαγράφει ένα τουρνουά από τη βάση δεδομένων"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        # Διαγραφή πρώτα τα Tournament_fee που σχετίζονται (λόγω Foreign Key)
        cursor.execute("DELETE FROM Tournament_fee WHERE tournament_id = ?", (tournament_id,))
        
        # Διαγραφή τουρνουά
        cursor.execute("DELETE FROM Tournament WHERE tournament_id = ?", (tournament_id,))
        
        # Ενημέρωση του sqlite_sequence για το Tournament
        cursor.execute("SELECT MAX(tournament_id) FROM Tournament")
        max_id = cursor.fetchone()[0]
        
        if max_id is not None:
            cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'Tournament'", (max_id,))
        else:
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'Tournament'")
        
        con.commit()
        con.close()
        
        return {"success": True}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

def get_tournament_participants(tournament_id):
    """Λαμβάνει τους συμμετέχοντες ενός τουρνουά"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute("""
            SELECT m.member_id, m.first_name, m.last_name, tf.cost
            FROM Member m
            JOIN Payment p ON m.member_id = p.member_id
            JOIN Tournament_fee tf ON p.payment_id = tf.payment_id
            WHERE tf.tournament_id = ?
            ORDER BY m.first_name
        """, (tournament_id,))
        participants = cursor.fetchall()
        con.close()
        
        return participants if participants else None
    
    except sqlite3.Error as e:
        return None

# ======================= MATCH OPERATIONS =======================

def insert_match(tournament_id, court_id, member1_id, member2_id, score, phase, start_datetime, end_datetime, winner_id, comment):
    """Εισάγει ένα νέο αγώνα στη βάση δεδομένων"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute(
            "INSERT INTO Match (tournament_id, court_id, member1_id, member2_id, score, phase, start_datetime, end_datetime, winner_id, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (tournament_id, court_id, member1_id, member2_id, score if score else "0-0", phase, start_datetime, end_datetime, winner_id, comment)
        )
        con.commit()
        match_id = cursor.lastrowid
        con.close()
        
        return {"success": True, "match_id": match_id}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

def get_match_by_id(match_id):
    """Λαμβάνει τα στοιχεία ενός αγώνα από το ID του"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute(
            "SELECT match_id, tournament_id, court_id, member1_id, member2_id, score, phase, start_datetime, end_datetime, winner_id, comment FROM Match WHERE match_id = ?",
            (match_id,)
        )
        match = cursor.fetchone()
        con.close()
        
        return match
    
    except sqlite3.Error as e:
        return None

def get_tournament_matches(tournament_id):
    """Λαμβάνει όλους τους αγώνες ενός τουρνουά"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute("""
            SELECT m.match_id, m.tournament_id, m.court_id, m.member1_id, m.member2_id, m.score, m.phase, m.start_datetime, m.end_datetime, m.winner_id, m.comment
            FROM Match m
            WHERE m.tournament_id = ?
            ORDER BY m.match_id ASC
        """, (tournament_id,))
        matches = cursor.fetchall()
        con.close()
        
        return matches if matches else None
    
    except sqlite3.Error as e:
        return None

def update_match(match_id, field, value):
    """Ενημερώνει ένα πεδίο ενός αγώνα"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        valid_fields = ["score", "phase", "start_datetime", "end_datetime", "winner_id", "comment"]
        if field not in valid_fields:
            return {"success": False, "error": "Μη έγκυρο πεδίο!"}
        
        query = f"UPDATE Match SET {field} = ? WHERE match_id = ?"
        cursor.execute(query, (value, match_id))
        con.commit()
        con.close()
        
        return {"success": True}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}

def delete_match(match_id):
    """Διαγράφει ένα αγώνα από τη βάση δεδομένων"""
    try:
        con = get_connection()
        cursor = con.cursor()
        
        # Διαγραφή αγώνα
        cursor.execute("DELETE FROM Match WHERE match_id = ?", (match_id,))
        
        # Ενημέρωση του sqlite_sequence για το Match
        cursor.execute("SELECT MAX(match_id) FROM Match")
        max_id = cursor.fetchone()[0]
        
        if max_id is not None:
            cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'Match'", (max_id,))
        else:
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'Match'")
        
        con.commit()
        con.close()
        
        return {"success": True}
    
    except sqlite3.Error as e:
        return {"success": False, "error": f"Σφάλμα βάσης δεδομένων: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Σφάλμα: {e}"}
