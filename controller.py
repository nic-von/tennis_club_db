import sys
from model import (select_table, get_table_names,create_member, get_member, update_member_field,
    create_court, schedule_maintenance,create_tournament, create_match, record_match_result, get_upcoming_tournaments, register_member_to_tournament,
    get_filtered_schedule, get_financial_stats, get_member_stats,get_lesson_availability, enroll_member_in_lesson, delete_orphan_payments,
    create_reservation, get_member_reservations, update_reservation, get_schedule
)
from view import (
    show_header, show_table, show_schedule, show_menu, 
    show_success, show_error, show_member_details, show_stats, show_tournaments
)

def admin_manage_members():
    while True:
        show_header("ΔΙΑΧΕΙΡΙΣΗ ΜΕΛΩΝ")
        print("1. Νέο Μέλος")
        print("2. Προβολή/Επεξεργασία Μέλους")
        print("0. Πίσω")
        res = input("-> ").strip()
        
        if res == '0': break
        
        try:
            if res == '1':
                data = {
                    'first_name': input("Όνομα: "), 'last_name': input("Επώνυμο: "),
                    'phone': input("Τηλέφωνο: "), 'mail': input("Email: "),
                    'address': input("Διεύθυνση: "), 'dob':input("Ημ. Γέννησης (YYYY-MM-DD): ")
                }
                mid = create_member(data['first_name'], data['last_name'], data['phone'], 
                                    data['mail'], data['address'], data['dob'])
                show_success(f"Μέλος δημιουργήθηκε με ID: {mid}")
            
            elif res == '2':
                mid = input("Δώσε ID Μέλους: ")
                member = get_member(mid)
                show_member_details(member)
                
                print("Θέλεις να επεξεργαστείς πεδίο; (Enter για όχι)")
                print("Πεδία: first_name, last_name, phone, mail, address, date_of_birth")
                field = input("Πεδίο: ").strip()
                if field:
                    val = input(f"Νέα τιμή για {field}: ")
                    update_member_field(mid, field, val)
                    show_success("Ενημερώθηκε.")
        except Exception as e:
            show_error(e)

def admin_manage_courts():
    while True:
        show_header("ΔΙΑΧΕΙΡΙΣΗ ΓΗΠΕΔΩΝ")
        print("1. Νέο Γήπεδο")
        print("2. Προγραμματισμός Συντήρησης")
        print("3. Προβολή Προγράμματος (Φίλτρα)")
        print("0. Πίσω")
        res = input("-> ").strip()

        if res == '0': break

        try:
            if res == '1':
                create_court(input("Τύπος: "), input("Σχόλια: "))
                show_success("Γήπεδο προστέθηκε.")
            elif res == '2':
                schedule_maintenance(input("ID Γηπέδου: "), input("Περιγραφή: "), 
                                     input("Έναρξη (YYYY-MM-DD HH:MM): "), input("Λήξη: "))
                show_success("Συντήρηση καταχωρήθηκε.")
            elif res == '3':
                cid = input("ID Γηπέδου (Enter για όλα): ").strip()
                date = input("Ημερομηνία YYYY-MM-DD (Enter για όλες): ").strip()
                cid = cid if cid else None
                date = date if date else None
                data = get_schedule(cid, date)
                show_schedule(data)
        except Exception as e:
            show_error(e)

def admin_manage_tournaments():
    while True:
        show_header("TOYPNOYA & ΑΓΩΝΕΣ")
        print("1. Νέο Τουρνουά")
        print("2. Προσθήκη Αγώνα")
        print("3. Καταγραφή Αποτελέσματος")
        print("0. Πίσω")
        res = input("-> ").strip()

        if res == '0': break
        try:
            if res == '1':
                create_tournament(input("Όνομα: "), input("Κατηγορία: "), input("Από: "), input("Έως: "))
                show_success("ΟΚ")
            elif res == '2':
                create_match(input("Tournament ID: "), input("Court ID: "), 
                             input("Member 1 ID: "), input("Member 2 ID: "), 
                             input("Start: "), input("End: "), input("Phase: "))
                show_success("Αγώνας δημιουργήθηκε.")
            elif res == '3':
                record_match_result(input("Match ID: "), input("Score (x-x): "), 
                                    input("Winner ID: "), input("Σχόλια: "))
                show_success("Αποτέλεσμα καταγράφηκε.")
        except Exception as e:
            show_error(e)

def menu_member():
    # Ζητάμε το Member ID μία φορά κατά την είσοδο για ευκολία
    mid = input("Παρακαλώ εισάγετε το Member ID σας για ταυτοποίηση: ").strip()
    
    while True:
        show_header(f"TENNIS CLUB - ΜΕΛΟΣ [ID: {mid}]")
        options = {
            "1": "Πρόγραμμα Γηπέδων (Schedule)",
            "2": "Διαθεσιμότητα Μαθημάτων",
            "3": "Εγγραφή σε Μάθημα",
            "4": "Κράτηση Γηπέδου (Reservation)",
            "5": "Οι Κρατήσεις μου / Τροποποίηση",
            "6": "Εγγραφή σε Τουρνουά",
            "x": "Αποσύνδεση"
        }
        show_menu(options)
        choice = input("Επιλογή: ").strip().lower()

        match choice:
            case '1':
                try: show_schedule(get_filtered_schedule())
                except Exception as e: show_error(e)
            
            case '2':
                try: show_table(get_lesson_availability())
                except Exception as e: show_error(e)
            
            case '3':
                try:
                    lesson=1
                    lesson_id=[]
                    while lesson != 0:    
                        lesson = int(input("ID Μαθήματος(0 για συνέχεια): "))
                        if lesson !=0:
                            lesson_id.append(lesson)
                    discount= float(input("Ποσοστό έκτπωσης(0.5/1): "))
                    amount = int( input("Ποσό πληρωμής:"))
                    cost = str(enroll_member_in_lesson(mid, lesson_id, discount, amount , input("Τρόπος πληρωμής(Cash/Card):")))
                    show_success("Εγγραφή επιτυχής! \n Κόστος: " +cost)
                except Exception as e: show_error(e)

            case '4': # Νέα Λειτουργία: Κράτηση
                try:
                    cid = input("ID Γηπέδου: ")
                    disc = float(input("Ποσοστό έκτπωσης(0.5/1): "))
                    start = input("Ώρα Έναρξης (YYYY-MM-DD HH:MM): ")
                    end = input("Ώρα Λήξης (YYYY-MM-DD HH:MM): ")
                    people = input("Αριθμός Ατόμων: ")
                    create_reservation(mid, cid, disc, start, end, people, input("Τρόπος πληρωμής(Cash/Card):"))
                    show_success("Η κράτηση ολοκληρώθηκε! Κόστος:" +str(15*disc))
                except Exception as e: show_error(e)

            case '5': # Νέα Λειτουργία: Προβολή & Edit Κρατήσεων
                try:
                    my_res = get_member_reservations(mid)
                    show_table(my_res)
                    if my_res:
                        action = input("Θέλετε να τροποποιήσετε κράτηση; (y/n): ").lower()
                        if action == 'y':
                            rid = input("ID Κράτησης: ")
                            nstart = input("Νέα Έναρξη: ")
                            nend = input("Νέα Λήξη: ")
                            update_reservation(rid, nstart, nend)
                            show_success("Η κράτηση ενημερώθηκε.")
                except Exception as e: show_error(e)

            case '6': #΅Εγραφή σε Τουρνουά
                try:
                    tours = get_upcoming_tournaments()
                    show_tournaments(tours)
                    if tours:
                        tid = input("Επιλέξτε ID Τουρνουά για εγγραφή (Enter για ακύρωση): ")
                        if tid:
                            disc = float(input("Ποσοστό έκτπωσης(0.5/1): "))
                            register_member_to_tournament(mid, tid, disc, input("Τρόπος πληρωμής(Cash/Card):"))
                            show_success("Εγγραφήκατε στο τουρνουά! Κόστος:" +str(12*disc))
                except Exception as e: show_error(e)

            case 'x': break
            case _: print("Μη έγκυρη επιλογή.")

def menu_admin():
    while True:
        show_header("TENNIS CLUB - ADMIN")
        options = {
            "1": "Διαχείριση Μελών (CRUD)",
            "2": "Διαχείριση Γηπέδων & Προγράμματος",
            "3": "Διαχείριση Τουρνουά",
            "4": "Οικονομικά & Στατιστικά",
            "5": "Προβολή Raw Πινάκων",
            "6": "Συντήρηση Βάσης (Cleanup)",
            "x": "Αποσύνδεση"
        }
        show_menu(options)
        choice = input("Επιλογή: ").strip().lower()

        match choice:
            case '1': admin_manage_members()
            case '2': admin_manage_courts()
            case '3': admin_manage_tournaments()
            case '4':
                print("\n[A] Στατιστικά Mελών (Status)")
                print("[B] Οικονομικά Στοιχεία")
                sub = input("-> ").upper()
                try:
                    if sub == 'A': show_table(get_member_stats())
                    else: show_stats(get_financial_stats())
                except Exception as e: show_error(e)
            case '5':
                tables = get_table_names()
                print("\nΔιαθέσιμοι Πίνακες:")
                for i, t in enumerate(tables): print(f"{i+1}. {t}")
                idx = input("Επιλέξτε (Enter για πίσω): ")
                if idx.isdigit() and 1 <= int(idx) <= len(tables):
                    try: show_table(select_table(tables[int(idx)-1]))
                    except Exception as e: show_error(e)
            case '6':
                try:
                    c = delete_orphan_payments()
                    show_success(f"Διαγράφηκαν {c} ορφανές πληρωμές.")
                except Exception as e: show_error(e)
            case 'x': break
            case _: print("Μη έγκυρη επιλογή.")

def admin_login():
    if input("Κωδικός Admin (admin): ") == "admin":
        menu_admin()
    else:
        show_error("Λάθος κωδικός.")

def main():
    while True:
        show_header("ΚΕΝΤΡΙΚΗ ΕΙΣΟΔΟΣ")
        print("1. Είσοδος Μέλους")
        print("2. Είσοδος Admin")
        print("x. Έξοδος")
        
        choice = input("Επιλογή: ").strip().lower()
        match choice:
            case '1': menu_member()
            case '2': admin_login()
            case 'x': 
                print("Έξοδος...")
                break
            case _: print("Λάθος επιλογή.")

if __name__ == "__main__":
    main()