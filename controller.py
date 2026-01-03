from model import insert_member, get_member_by_id, update_member, get_stats, get_future_program, get_all_courts, insert_court, get_court_by_id, update_court, delete_court, insert_maintenance, get_maintenance_by_id, update_maintenance, delete_maintenance, get_all_tournaments, insert_tournament, get_tournament_by_id, update_tournament, delete_tournament, get_tournament_participants, insert_match, get_match_by_id, get_tournament_matches, update_match, delete_match
from view import (
    clear_screen, print_menu, print_table, print_member_info, 
    print_success, print_error, print_info, print_edit_menu, 
    print_exit_message, print_invalid_choice, print_separator, print_program_statistics_menu, print_program_table, print_court_info_menu, print_tournament_menu
)

def register_new_member():
    """Ελέγχει την εγγραφή νέου μέλους"""
    clear_screen()
    print("=== ΕΓΓΡΑΦΗ ΝΕΟΥ ΜΕΛΟΥΣ ===\n")
    
    try:
        first_name = input("Όνομα: ").strip()
        if not first_name:
            print_error("Το όνομα δεν μπορεί να είναι κενό!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        last_name = input("Επώνυμο: ").strip()
        if not last_name:
            print_error("Το επώνυμο δεν μπορεί να είναι κενό!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        phone = input("Τηλέφωνο: ").strip()
        if not phone:
            print_error("Το τηλέφωνο δεν μπορεί να είναι κενό!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        mail = input("Email: ").strip()
        if not mail:
            print_error("Το email δεν μπορεί να είναι κενό!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        address = input("Διεύθυνση: ").strip()
        if not address:
            print_error("Η διεύθυνση δεν μπορεί να είναι κενή!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        date_of_birth = input("Ημερομηνία Γέννησης (YYYY-MM-DD): ").strip()
        if not date_of_birth:
            print_error("Η ημερομηνία γέννησης δεν μπορεί να είναι κενή!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        # Κλήση model function
        result = insert_member(first_name, last_name, phone, mail, address, date_of_birth)
        
        if result["success"]:
            print_success("Το μέλος εγγράφηκε με επιτυχία!")
            print(f"  ID Μέλους: {result['member_id']}")
            print(f"  Όνομα: {first_name} {last_name}")
            print(f"  Τηλέφωνο: {phone}")
            print(f"  Email: {mail}")
            print(f"  Διεύθυνση: {address}")
            print(f"  Ημερομηνία Γέννησης: {date_of_birth}")
        else:
            print_error(result["error"])
    
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε στο μενού...")

def edit_member_data():
    """Ελέγχει την επεξεργασία στοιχείων μέλους"""
    clear_screen()
    print("=== ΕΠΕΞΕΡΓΑΣΙΑ ΣΤΟΙΧΕΙΩΝ ΜΕΛΟΥΣ ===\n")
    
    try:
        member_id = input("Δώστε το ID του μέλους: ").strip()
        
        if not member_id.isdigit():
            print_error("Το ID πρέπει να είναι αριθμός!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        # Κλήση model function
        member = get_member_by_id(member_id)
        
        if not member:
            print_error(f"Δεν βρέθηκε μέλος με ID {member_id}!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        print_member_info(member)
        print_edit_menu()
        
        choice = input("Επιλέξτε (1-7): ").strip()
        
        field_map = {
            "1": "first_name",
            "2": "last_name",
            "3": "phone",
            "4": "mail",
            "5": "address",
            "6": "date_of_birth"
        }
        
        if choice in field_map:
            field = field_map[choice]
            prompt = {
                "first_name": "Δώστε το νέο όνομα: ",
                "last_name": "Δώστε το νέο επώνυμο: ",
                "phone": "Δώστε το νέο τηλέφωνο: ",
                "mail": "Δώστε το νέο email: ",
                "address": "Δώστε τη νέα διεύθυνση: ",
                "date_of_birth": "Δώστε τη νέα ημερομηνία γέννησης (YYYY-MM-DD): "
            }
            
            new_value = input(prompt[field]).strip()
            if new_value:
                result = update_member(member_id, field, new_value)
                if result["success"]:
                    print_success("Τα στοιχεία ενημερώθηκαν με επιτυχία!")
                else:
                    print_error(result["error"])
        
        elif choice == "7":
            print_info("Ακύρωση.")
        else:
            print_invalid_choice()
        
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε στο μενού...")

def manage_member():
    """Διαχείριση κρατήσεων και πληρωμών"""
    clear_screen()
    print("=== ΔΙΑΧΕΙΡΙΣΗ ΜΕΛΟΥΣ (ΚΡΑΤΗΣΕΙΣ/ΠΛΗΡΩΜΕΣ) ===\n")
    print("Αυτή η λειτουργία θα υλοποιηθεί σύντομα...")
    input("\nΠατήστε Enter για να επιστρέψετε στο μενού...")

def program_statistics():
    """Πρόγραμμα & Οικονομικά Στατιστικά"""
    while True:
        clear_screen()
        print_program_statistics_menu()
        
        choice = input("Επιλέξτε μια λειτουργία (1-5): ").strip()
        
        if choice == "1":
            display_program()
        elif choice == "2":
            display_tournaments()
        elif choice == "3":
            display_court_info()
        elif choice == "4":
            display_statistics()
        elif choice == "5":
            break
        else:
            print_invalid_choice()
            input("Πατήστε Enter για να συνεχίσετε...")

def display_program():
    """Εμφάνιση προγράμματος"""
    clear_screen()
    print("=== ΕΜΦΑΝΙΣΗ ΠΡΟΓΡΑΜΜΑΤΟΣ ===\n")
    
    try:
        # Ερώτηση για ημερομηνία
        print("Δώστε την ημερομηνία έναρξης (μορφή: YYYY-MM-DD)")
        print("(Γράψτε 'all' για όλο το πρόγραμμα)")
        start_date_input = input("Ημερομηνία: ").strip()
        
        start_date = None if start_date_input.lower() == "all" else start_date_input
        
        # Ερώτηση για γήπεδο
        print("\nΔώστε το ID του γηπέδου")
        print("(Γράψτε 'all' για όλα τα γήπεδα)")
        court_input = input("Γήπεδο: ").strip()
        
        court_id = None if court_input.lower() == "all" else (int(court_input) if court_input.isdigit() else None)
        
        if court_input.isdigit() == False and court_input.lower() != "all":
            print_error("Μη έγκυρο ID γηπέδου!")
            input("Πατήστε Enter για να επιστρέψετε...")
            return
        
        # Ερώτηση για τύπο δραστηριότητας
        print("\nΕπιλέξτε τύπο δραστηριότητας:")
        print("1. Μαθήματα (Lesson)")
        print("2. Συντήρηση (Maintenance)")
        print("3. Αγώνες (Match)")
        print("4. Κρατήσεις (Reservation)")
        print("5. Όλα")
        print("-" * 30)
        activity_choice = input("Επιλέξτε (1-5): ").strip()
        
        activity_map = {
            "1": "Lesson",
            "2": "Maintenance",
            "3": "Match",
            "4": "Reservation"
        }
        
        activity_type = activity_map.get(activity_choice) if activity_choice in activity_map else None
        
        if activity_choice not in ["1", "2", "3", "4", "5"]:
            print_error("Μη έγκυρη επιλογή!")
            input("Πατήστε Enter για να επιστρέψετε...")
            return
        
        # Κλήση model function
        results = get_future_program(start_date, court_id, activity_type)
        
        clear_screen()
        print("=== ΠΡΟΓΡΑΜΜΑ ΓΗΠΕΔΩΝ ===\n")
        
        if results:
            print_program_table(None, results)
        else:
            print_info("Δεν υπάρχουν προγράμματα για τα κριτήρια που επιλέξατε.")
    
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε...")

def display_tournaments():
    """Εμφάνιση τουρνουά"""
    while True:
        clear_screen()
        print_tournament_menu()
        
        choice = input("Επιλέξτε μια λειτουργία (1-4): ").strip()
        
        if choice == "1":
            view_tournaments()
        elif choice == "2":
            add_tournament()
        elif choice == "3":
            manage_tournament()
        elif choice == "4":
            break
        else:
            print_invalid_choice()
            input("Πατήστε Enter για να συνεχίσετε...")

def view_tournaments():
    """Προβολή όλων των τουρνουά"""
    clear_screen()
    print("=== ΠΡΟΒΟΛΗ ΤΟΥΡΝΟΥΑ ===\n")
    
    try:
        tournaments = get_all_tournaments()
        
        if tournaments:
            print("=" * 100)
            print(f"{'ID':<5} | {'Όνομα':<30} | {'Κατηγορία':<20} | {'Έναρξη':<15} | {'Λήξη':<15}")
            print("=" * 100)
            
            for tournament in tournaments:
                tournament_id = tournament[0]
                name = tournament[1] if tournament[1] else "-"
                category = tournament[2] if tournament[2] else "-"
                start_date = tournament[3] if tournament[3] else "-"
                end_date = tournament[4] if tournament[4] else "-"
                
                # Κόψτε το όνομα αν είναι πολύ μεγάλο
                name_str = name[:28] if len(str(name)) > 28 else name
                
                print(f"{tournament_id:<5} | {name_str:<30} | {category:<20} | {start_date:<15} | {end_date:<15}")
            
            print("=" * 100 + "\n")
        else:
            print_info("Δεν υπάρχουν τουρνουά στη βάση δεδομένων.")
    
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε...")

def add_tournament():
    """Δημιουργία νέου τουρνουά"""
    clear_screen()
    print("=== ΔΗΜΙΟΥΡΓΙΑ ΝΕΟΥ ΤΟΥΡΝΟΥΑ ===\n")
    
    try:
        name = input("Όνομα Τουρνουά: ").strip()
        if not name:
            print_error("Το όνομα δεν μπορεί να είναι κενό!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        category = input("Κατηγορία: ").strip()
        if not category:
            print_error("Η κατηγορία δεν μπορεί να είναι κενή!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        start_date = input("Ημερομηνία Έναρξης (YYYY-MM-DD): ").strip()
        if not start_date:
            print_error("Η ημερομηνία έναρξης δεν μπορεί να είναι κενή!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        end_date = input("Ημερομηνία Λήξης (YYYY-MM-DD): ").strip()
        if not end_date:
            print_error("Η ημερομηνία λήξης δεν μπορεί να είναι κενή!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        # Κλήση model function
        result = insert_tournament(name, category, start_date, end_date)
        
        if result["success"]:
            print_success("Το τουρνουά δημιουργήθηκε με επιτυχία!")
            print(f"  ID Τουρνουά: {result['tournament_id']}")
            print(f"  Όνομα: {name}")
            print(f"  Κατηγορία: {category}")
            print(f"  Έναρξη: {start_date}")
            print(f"  Λήξη: {end_date}")
        else:
            print_error(result["error"])
    
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε...")

def manage_tournament():
    """Διαχείριση τουρνουά"""
    clear_screen()
    print("=== ΔΙΑΧΕΙΡΙΣΗ ΤΟΥΡΝΟΥΑ ===\n")
    
    try:
        tournament_id = input("Δώστε το ID του τουρνουά: ").strip()
        
        if not tournament_id.isdigit():
            print_error("Το ID πρέπει να είναι αριθμός!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        # Κλήση model function
        tournament = get_tournament_by_id(tournament_id)
        
        if not tournament:
            print_error(f"Δεν βρέθηκε τουρνουά με ID {tournament_id}!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        print(f"\nΤρέχοντα στοιχεία:")
        print(f"  ID: {tournament[0]}")
        print(f"  Όνομα: {tournament[1]}")
        print(f"  Κατηγορία: {tournament[2]}")
        print(f"  Έναρξη: {tournament[3]}")
        print(f"  Λήξη: {tournament[4]}\n")
        
        print("\nΤι θέλετε να επεξεργαστείτε;")
        print("1. Όνομα")
        print("2. Κατηγορία")
        print("3. Ημερομηνία Έναρξης")
        print("4. Ημερομηνία Λήξης")
        print("5. Προβολή Συμμετεχόντων")
        print("6. Προσθήκη Αγώνων")
        print("7. Προβολή Αγώνων")
        print("8. Διαγραφή Τουρνουά")
        print("9. Ακύρωση")
        print("-" * 30)
        
        choice = input("Επιλέξτε (1-9): ").strip()
        
        if choice == "1":
            new_name = input("Δώστε το νέο όνομα: ").strip()
            if new_name:
                result = update_tournament(tournament_id, "name", new_name)
                if result["success"]:
                    print_success("Το όνομα ενημερώθηκε με επιτυχία!")
                else:
                    print_error(result["error"])
        
        elif choice == "2":
            new_category = input("Δώστε τη νέα κατηγορία: ").strip()
            if new_category:
                result = update_tournament(tournament_id, "category", new_category)
                if result["success"]:
                    print_success("Η κατηγορία ενημερώθηκε με επιτυχία!")
                else:
                    print_error(result["error"])
        
        elif choice == "3":
            new_start = input("Δώστε τη νέα ημερομηνία έναρξης (YYYY-MM-DD): ").strip()
            if new_start:
                result = update_tournament(tournament_id, "start_date", new_start)
                if result["success"]:
                    print_success("Η ημερομηνία έναρξης ενημερώθηκε με επιτυχία!")
                else:
                    print_error(result["error"])
        
        elif choice == "4":
            new_end = input("Δώστε τη νέα ημερομηνία λήξης (YYYY-MM-DD): ").strip()
            if new_end:
                result = update_tournament(tournament_id, "end_date", new_end)
                if result["success"]:
                    print_success("Η ημερομηνία λήξης ενημερώθηκε με επιτυχία!")
                else:
                    print_error(result["error"])
        
        elif choice == "5":
            # Προβολή συμμετεχόντων
            participants = get_tournament_participants(tournament_id)
            if participants:
                print("\n" + "=" * 80)
                print(f"Συμμετέχοντες στο Τουρνουά ID {tournament_id}:")
                print("=" * 80)
                print(f"{'ID Μέλους':<12} | {'Όνομα':<20} | {'Επώνυμο':<20} | {'Κόστος':<10}")
                print("=" * 80)
                for participant in participants:
                    member_id = participant[0]
                    first_name = participant[1]
                    last_name = participant[2]
                    cost = participant[3]
                    print(f"{member_id:<12} | {first_name:<20} | {last_name:<20} | {cost:<10}")
                print("=" * 80 + "\n")
            else:
                print_info("Δεν υπάρχουν συμμετέχοντες σε αυτό το τουρνουά.")
        
        elif choice == "6":
            add_match(tournament_id)
        
        elif choice == "7":
            view_tournament_matches(tournament_id)
        
        elif choice == "8":
            confirm = input(f"Είστε σίγουροι ότι θέλετε να διαγράψετε το τουρνουά {tournament_id}; (yes/no): ").strip().lower()
            if confirm == "yes":
                result = delete_tournament(tournament_id)
                if result["success"]:
                    print_success("Το τουρνουά διαγράφηκε με επιτυχία!")
                else:
                    print_error(result["error"])
            else:
                print_info("Η διαγραφή ακυρώθηκε.")
        
        elif choice == "9":
            print_info("Ακύρωση.")
        else:
            print_invalid_choice()
        
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε...")

def add_match(tournament_id):
    """Προσθήκη νέου αγώνα σε τουρνουά"""
    clear_screen()
    print(f"=== ΠΡΟΣΘΗΚΗ ΑΓΩΝΑ - ΤΟΥΡΝΟΥΑ {tournament_id} ===\n")
    
    try:
        court_id = input("ID Γηπέδου: ").strip()
        if not court_id.isdigit():
            print_error("Το ID γηπέδου πρέπει να είναι αριθμός!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        member1_id = input("ID Μέλους 1: ").strip()
        if not member1_id.isdigit():
            print_error("Το ID μέλους 1 πρέπει να είναι αριθμός!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        member2_id = input("ID Μέλους 2 (προαιρετικό): ").strip()
        member2_id = int(member2_id) if member2_id.isdigit() else None
        
        score = input("Σκορ (προαιρετικό, π.χ. 6-4): ").strip()
        score = score if score else "0-0"
        
        phase = input("Φάση (π.χ. Ημιτελικά, Τελικός): ").strip()
        if not phase:
            print_error("Η φάση δεν μπορεί να είναι κενή!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        start_datetime = input("Ημερομηνία/Ώρα Έναρξης (YYYY-MM-DD HH:MM:SS): ").strip()
        if not start_datetime:
            print_error("Η ημερομηνία έναρξης δεν μπορεί να είναι κενή!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        end_datetime = input("Ημερομηνία/Ώρα Λήξης (YYYY-MM-DD HH:MM:SS): ").strip()
        if not end_datetime:
            print_error("Η ημερομηνία λήξης δεν μπορεί να είναι κενή!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        winner_id = input("ID Νικητή (προαιρετικό): ").strip()
        winner_id = int(winner_id) if winner_id.isdigit() else None
        
        comment = input("Σχόλιο (προαιρετικό): ").strip()
        comment = comment if comment else None
        
        # Κλήση model function
        result = insert_match(tournament_id, court_id, member1_id, member2_id, score, phase, start_datetime, end_datetime, winner_id, comment)
        
        if result["success"]:
            print_success("Ο αγώνας προστέθηκε με επιτυχία!")
            print(f"  ID Αγώνα: {result['match_id']}")
            print(f"  Τουρνουά: {tournament_id}")
            print(f"  Γήπεδο: {court_id}")
            print(f"  Μέλος 1: {member1_id}")
            if member2_id:
                print(f"  Μέλος 2: {member2_id}")
            print(f"  Σκορ: {score}")
            print(f"  Φάση: {phase}")
        else:
            print_error(result["error"])
    
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε...")

def view_tournament_matches(tournament_id):
    """Προβολή αγώνων τουρνουά"""
    clear_screen()
    print(f"=== ΑΓΩΝΕΣ ΤΟΥΡΝΟΥΑ {tournament_id} ===\n")
    
    try:
        matches = get_tournament_matches(tournament_id)
        
        if matches:
            print("=" * 140)
            print(f"{'ID':<5} | {'Γήπεδο':<8} | {'Μέλος 1':<10} | {'Μέλος 2':<10} | {'Σκορ':<8} | {'Φάση':<15} | {'Έναρξη':<20} | {'Λήξη':<20} | {'Νικητής':<8}")
            print("=" * 140)
            
            for match in matches:
                match_id = match[0]
                court_id = match[2]
                member1_id = match[3]
                member2_id = match[4] if match[4] else "-"
                score = match[5] if match[5] else "-"
                phase = match[6] if match[6] else "-"
                start_datetime = match[7] if match[7] else "-"
                end_datetime = match[8] if match[8] else "-"
                winner_id = match[9] if match[9] else "-"
                
                print(f"{match_id:<5} | {court_id:<8} | {member1_id:<10} | {str(member2_id):<10} | {score:<8} | {phase:<15} | {str(start_datetime):<20} | {str(end_datetime):<20} | {str(winner_id):<8}")
            
            print("=" * 140 + "\n")
        else:
            print_info("Δεν υπάρχουν αγώνες σε αυτό το τουρνουά.")
    
    except Exception as e:
        print_error(f"Σφάλμα: {e}")

def display_court_info():
    """Εμφάνιση πληροφοριών γηπέδων"""
    while True:
        clear_screen()
        print_court_info_menu()
        
        choice = input("Επιλέξτε μια λειτουργία (1-6): ").strip()
        
        if choice == "1":
            view_courts()
        elif choice == "2":
            add_court()
        elif choice == "3":
            edit_court()
        elif choice == "4":
            add_maintenance()
        elif choice == "5":
            edit_maintenance()
        elif choice == "6":
            break
        else:
            print_invalid_choice()
            input("Πατήστε Enter για να συνεχίσετε...")

def view_courts():
    """Προβολή όλων των γηπέδων"""
    clear_screen()
    print("=== ΠΡΟΒΟΛΗ ΓΗΠΕΔΩΝ ===\n")
    
    try:
        courts = get_all_courts()
        
        if courts:
            print("=" * 80)
            print(f"{'ID':<5} | {'Τύπος':<30} | {'Σχόλια':<40}")
            print("=" * 80)
            
            for court in courts:
                court_id = court[0]
                court_type = court[1] if court[1] else "-"
                comments = court[2] if court[2] else "-"
                
                # Περικόπτω τα σχόλια αν είναι πολύ μεγάλα
                comments_str = comments[:38] if len(str(comments)) > 38 else comments
                
                print(f"{court_id:<5} | {court_type:<30} | {comments_str:<40}")
            
            print("=" * 80 + "\n")
        else:
            print_info("Δεν υπάρχουν γήπεδα στη βάση δεδομένων.")
    
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε...")

def add_court():
    """Προσθήκη νέου γηπέδου"""
    clear_screen()
    print("=== ΠΡΟΣΘΗΚΗ ΝΕΟΥ ΓΗΠΕΔΟΥ ===\n")
    
    try:
        court_type = input("Τύπος Γηπέδου: ").strip()
        if not court_type:
            print_error("Ο τύπος γηπέδου δεν μπορεί να είναι κενός!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        comments = input("Σχόλια (προαιρετικό): ").strip()
        comments = comments if comments else None
        
        # Κλήση model function
        result = insert_court(court_type, comments)
        
        if result["success"]:
            print_success("Το γήπεδο προστέθηκε με επιτυχία!")
            print(f"  ID Γηπέδου: {result['court_id']}")
            print(f"  Τύπος: {court_type}")
            if comments:
                print(f"  Σχόλια: {comments}")
        else:
            print_error(result["error"])
    
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε...")

def edit_court():
    """Επεξεργασία γηπέδου"""
    clear_screen()
    print("=== ΕΠΕΞΕΡΓΑΣΙΑ ΓΗΠΕΔΟΥ ===\n")
    
    try:
        court_id = input("Δώστε το ID του γηπέδου: ").strip()
        
        if not court_id.isdigit():
            print_error("Το ID πρέπει να είναι αριθμός!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        # Κλήση model function
        court = get_court_by_id(court_id)
        
        if not court:
            print_error(f"Δεν βρέθηκε γήπεδο με ID {court_id}!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        print(f"\nΤρέχοντα στοιχεία:")
        print(f"  ID: {court[0]}")
        print(f"  Τύπος: {court[1]}")
        print(f"  Σχόλια: {court[2] if court[2] else '-'}\n")
        
        print("\nΤι θέλετε να επεξεργαστείτε;")
        print("1. Τύπος")
        print("2. Σχόλια")
        print("3. Διαγραφή Γηπέδου")
        print("4. Ακύρωση")
        print("-" * 30)
        
        choice = input("Επιλέξτε (1-4): ").strip()
        
        if choice == "1":
            new_type = input("Δώστε τον νέο τύπο: ").strip()
            if new_type:
                result = update_court(court_id, "Type", new_type)
                if result["success"]:
                    print_success("Ο τύπος ενημερώθηκε με επιτυχία!")
                else:
                    print_error(result["error"])
        
        elif choice == "2":
            new_comments = input("Δώστε τα νέα σχόλια: ").strip()
            result = update_court(court_id, "comments", new_comments if new_comments else None)
            if result["success"]:
                print_success("Τα σχόλια ενημερώθηκαν με επιτυχία!")
            else:
                print_error(result["error"])
        
        elif choice == "3":
            confirm = input(f"Είστε σίγουροι ότι θέλετε να διαγράψετε το γήπεδο {court_id}; (yes/no): ").strip().lower()
            if confirm == "yes":
                result = delete_court(court_id)
                if result["success"]:
                    print_success("Το γήπεδο διαγράφηκε με επιτυχία!")
                else:
                    print_error(result["error"])
            else:
                print_info("Η διαγραφή ακυρώθηκε.")
        
        elif choice == "4":
            print_info("Ακύρωση.")
        else:
            print_invalid_choice()
        
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε...")

def add_maintenance():
    """Προσθήκη συντήρησης"""
    clear_screen()
    print("=== ΠΡΟΣΘΗΚΗ ΣΥΝΤΗΡΗΣΗΣ ===\n")
    
    try:
        court_id = input("ID Γηπέδου: ").strip()
        if not court_id.isdigit():
            print_error("Το ID γηπέδου πρέπει να είναι αριθμός!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        start_datetime = input("Ημερομηνία/Ώρα Έναρξης (YYYY-MM-DD HH:MM:SS): ").strip()
        if not start_datetime:
            print_error("Η ημερομηνία έναρξης δεν μπορεί να είναι κενή!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        description = input("Περιγραφή: ").strip()
        description = description if description else None
        
        # Κλήση model function (end_datetime = NULL)
        result = insert_maintenance(court_id, start_datetime, description)
        
        if result["success"]:
            print_success("Η συντήρηση προστέθηκε με επιτυχία!")
            print(f"  ID Συντήρησης: {result['maintenance_id']}")
            print(f"  Γήπεδο: {court_id}")
            print(f"  Έναρξη: {start_datetime}")
            print(f"  Λήξη: NULL (δεν έχει ολοκληρωθεί)")
            if description:
                print(f"  Περιγραφή: {description}")
        else:
            print_error(result["error"])
    
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε...")

def edit_maintenance():
    """Επεξεργασία συντήρησης"""
    clear_screen()
    print("=== ΕΠΕΞΕΡΓΑΣΙΑ ΣΥΝΤΗΡΗΣΗΣ ===\n")
    
    try:
        maintenance_id = input("Δώστε το ID της συντήρησης: ").strip()
        
        if not maintenance_id.isdigit():
            print_error("Το ID πρέπει να είναι αριθμός!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        # Κλήση model function
        maintenance = get_maintenance_by_id(maintenance_id)
        
        if not maintenance:
            print_error(f"Δεν βρέθηκε συντήρηση με ID {maintenance_id}!")
            input("Πατήστε Enter για να συνεχίσετε...")
            return
        
        print(f"\nΤρέχοντα στοιχεία:")
        print(f"  ID: {maintenance[0]}")
        print(f"  Γήπεδο: {maintenance[1]}")
        print(f"  Έναρξη: {maintenance[2]}")
        print(f"  Λήξη: {maintenance[3] if maintenance[3] else 'NULL (δεν έχει ολοκληρωθεί)'}")
        print(f"  Περιγραφή: {maintenance[4] if maintenance[4] else '-'}\n")
        
        print("\nΤι θέλετε να επεξεργαστείτε;")
        print("1. Γήπεδο")
        print("2. Ημερομηνία/Ώρα Έναρξης")
        print("3. Ημερομηνία/Ώρα Λήξης")
        print("4. Περιγραφή")
        print("5. Διαγραφή Συντήρησης")
        print("6. Ακύρωση")
        print("-" * 30)
        
        choice = input("Επιλέξτε (1-6): ").strip()
        
        if choice == "1":
            new_court_id = input("Δώστε το νέο ID γηπέδου: ").strip()
            if new_court_id and new_court_id.isdigit():
                result = update_maintenance(maintenance_id, "court_id", new_court_id)
                if result["success"]:
                    print_success("Το γήπεδο ενημερώθηκε με επιτυχία!")
                else:
                    print_error(result["error"])
        
        elif choice == "2":
            new_start = input("Δώστε τη νέα ημερομηνία/ώρα έναρξης (YYYY-MM-DD HH:MM:SS): ").strip()
            if new_start:
                result = update_maintenance(maintenance_id, "start_datetime", new_start)
                if result["success"]:
                    print_success("Η ημερομηνία έναρξης ενημερώθηκε με επιτυχία!")
                else:
                    print_error(result["error"])
        
        elif choice == "3":
            new_end = input("Δώστε τη νέα ημερομηνία/ώρα λήξης (YYYY-MM-DD HH:MM:SS ή κενό για NULL): ").strip()
            result = update_maintenance(maintenance_id, "end_datetime", new_end)
            if result["success"]:
                print_success("Η ημερομηνία λήξης ενημερώθηκε με επιτυχία!")
            else:
                print_error(result["error"])
        
        elif choice == "4":
            new_description = input("Δώστε τη νέα περιγραφή: ").strip()
            result = update_maintenance(maintenance_id, "description", new_description if new_description else None)
            if result["success"]:
                print_success("Η περιγραφή ενημερώθηκε με επιτυχία!")
            else:
                print_error(result["error"])
        
        elif choice == "5":
            confirm = input(f"Είστε σίγουροι ότι θέλετε να διαγράψετε τη συντήρηση {maintenance_id}; (yes/no): ").strip().lower()
            if confirm == "yes":
                result = delete_maintenance(maintenance_id)
                if result["success"]:
                    print_success("Η συντήρηση διαγράφηκε με επιτυχία!")
                else:
                    print_error(result["error"])
            else:
                print_info("Η διαγραφή ακυρώθηκε.")
        
        elif choice == "6":
            print_info("Ακύρωση.")
        else:
            print_invalid_choice()
        
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε...")

def display_statistics():
    """Εμφάνιση στατιστικών"""
    clear_screen()
    print("=== ΣΤΑΤΙΣΤΙΚΑ ===\n")
    
    try:
        stats = get_stats()
        
        if "error" in stats:
            print_error(stats["error"])
        else:
            print(f"Συνολικά μέλη: {stats['total_members']}")
            print(f"Συνολικές πληρωμές: €{stats['total_payments']:.2f}")
    
    except Exception as e:
        print_error(f"Σφάλμα: {e}")
    
    input("\nΠατήστε Enter για να επιστρέψετε...")

def main():
    """Κύριο loop του controller"""
    while True:
        clear_screen()
        print_menu()
        
        choice = input("Επιλέξτε μια λειτουργία (1-5): ").strip()
        
        if choice == "1":
            register_new_member()
        elif choice == "2":
            edit_member_data()
        elif choice == "3":
            manage_member()
        elif choice == "4":
            program_statistics()
        elif choice == "5":
            print_exit_message()
            break
        else:
            clear_screen()
            print_menu()
            print_invalid_choice()
            input("Πατήστε Enter για να συνεχίσετε...")

if __name__ == "__main__":
    main()
