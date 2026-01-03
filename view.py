import os

def clear_screen():
    """Καθαρίζει την οθόνη"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """Εμφανίζει το κύριο μενού"""
    print("=" * 50)
    print("    TENNIS CLUB MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. Εγγραφή Νέου Μέλους")
    print("2. Επεξεργασία Στοιχείων Μέλους")
    print("3. Διαχείριση Μέλους (Κρατήσεις/Πληρωμές)")
    print("4. Πρόγραμμα & Διαχείρηση & Οικονομικά Στατιστικά")
    print("5. Έξοδος")
    print("-" * 50)

def print_table(headers, rows):
    """Εμφανίζει δεδομένα σε μορφή πίνακα"""
    if not rows:
        print("Δεν υπάρχουν δεδομένα για εμφάνιση.")
        return
    
    # Υπολογισμός πλάτους στηλών
    col_widths = [len(str(header)) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Εμφάνιση headers
    header_line = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))
    
    # Εμφάνιση rows
    for row in rows:
        row_line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print(row_line)

def print_member_info(member):
    """Εμφανίζει πληροφορίες μέλους"""
    if member:
        print(f"\nΤρέχοντα στοιχεία:")
        print(f"  ID: {member[0]}")
        print(f"  Όνομα: {member[1]}")
        print(f"  Επώνυμο: {member[2]}")
        print(f"  Τηλέφωνο: {member[3]}")
        print(f"  Email: {member[4]}")
        print(f"  Διεύθυνση: {member[5]}")
        print(f"  Ημερομηνία Γέννησης: {member[6]}\n")
    else:
        print("Δεν βρέθηκαν πληροφορίες μέλους.")

def print_success(message):
    """Εμφανίζει μήνυμα επιτυχίας"""
    print(f"\n✓ {message}")

def print_error(message):
    """Εμφανίζει μήνυμα σφάλματος"""
    print(f"\n✗ {message}")

def print_info(message):
    """Εμφανίζει πληροφοριακό μήνυμα"""
    print(f"\nℹ {message}")

def print_edit_menu():
    """Εμφανίζει το μενού επεξεργασίας μέλους"""
    print("\nΤι θέλετε να επεξεργαστείτε;")
    print("1. Όνομα")
    print("2. Επώνυμο")
    print("3. Τηλέφωνο")
    print("4. Email")
    print("5. Διεύθυνση")
    print("6. Ημερομηνία Γέννησης")
    print("7. Ακύρωση")
    print("-" * 30)

def print_exit_message():
    """Εμφανίζει μήνυμα εξόδου"""
    clear_screen()
    print("Ευχαριστώ που χρησιμοποιήσατε το σύστημα!")
    print("Έξοδος...")

def print_invalid_choice():
    """Εμφανίζει μήνυμα για μη έγκυρη επιλογή"""
    print("\nΜη έγκυρη επιλογή! Παρακαλώ επιλέξτε ξανά.")

def print_separator():
    """Εμφανίζει διαχωριστικό"""
    print("\n" + "=" * 50 + "\n")

def print_court_info_menu():
    """Εμφανίζει το μενού Πληροφοριών Γηπέδων"""
    print("=" * 50)
    print("  ΠΛΗΡΟΦΟΡΙΕΣ ΓΗΠΕΔΩΝ")
    print("=" * 50)
    print("1. Προβολή Γηπέδων")
    print("2. Προσθήκη Γηπέδου")
    print("3. Επεξεργασία Γηπέδου")
    print("4. Προσθήκη Συντήρησης")
    print("5. Επεξεργασία Συντήρησης")
    print("6. Επιστροφή στο Κύριο Μενού")
    print("-" * 50)

def print_program_statistics_menu():
    """Εμφανίζει το μενού Προγράμματος & Διαχείρησης & Στατιστικών"""
    print("=" * 50)
    print("  ΠΡΟΓΡΑΜΜΑ & ΔΙΑΧΕΙΡΙΣΗ & ΟΙΚΟΝΟΜΙΚΑ ΣΤΑΤΙΣΤΙΚΑ")
    print("=" * 50)
    print("1. Εμφάνιση Προγράμματος")
    print("2. Τουρνουά")
    print("3. Πληροφορίες Γηπέδων")
    print("4. Στατιστικά")
    print("5. Επιστροφή στο Κύριο Μενού")
    print("-" * 50)

def print_program_table(headers, rows):
    """Εμφανίζει το πρόγραμμα και δραστηριότητες σε μορφή πίνακα"""
    if not rows:
        print("Δεν υπάρχουν προγράμματα για τα κριτήρια που επιλέξατε.")
        return
    
    # Προσαρμοσμένα headers για το Global_Court_Schedule
    print("\n" + "=" * 140)
    print(f"{'Activity':<15} | {'Court':<6} | {'Έναρξη':<20} | {'Λήξη':<20} | {'Λεπτομέρειες':<50}")
    print("=" * 140)
    
    for row in rows:
        # Σειρά στο VIEW: court_id, Activity, start_datetime, end_datetime, Details
        court_id = row[0] if row[0] is not None else "-"
        activity = row[1] if row[1] is not None else "-"
        start_datetime = row[2] if row[2] is not None else "-"
        end_datetime = row[3] if row[3] is not None else "-"
        details = row[4] if row[4] is not None else "-"
        
        # Κόψτε τα details αν είναι πολύ μεγάλα
        details_str = str(details)[:48] if details != "-" else "-"
        
        print(f"{activity:<15} | {court_id:<6} | {start_datetime:<20} | {end_datetime:<20} | {details_str:<50}")
    
    print("=" * 140 + "\n")

def print_tournament_menu():
    """Εμφανίζει το μενού Τουρνουά"""
    print("=" * 50)
    print("  ΤΟΥΡΝΟΥΑ")
    print("=" * 50)
    print("1. Προβολή Τουρνουά")
    print("2. Δημιουργία Τουρνουά")
    print("3. Διαχείριση Τουρνουά")
    print("4. Επιστροφή στο Κύριο Μενού")
    print("-" * 50)
