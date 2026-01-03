import sys
from model import (get_table_names, select_table, get_member_stats, 
                   get_lesson_availability, enroll_member_in_lesson, 
                   delete_orphan_payments)
from view import show_header, show_table, show_menu, show_success, show_error

def view_tables_menu():
    """Υπο-μενού για προβολή raw πινάκων"""
    tables = get_table_names()
    while True:
        show_header("ΠΡΟΒΟΛΗ ΠΙΝΑΚΩΝ")
        options = {str(i+1): t for i, t in enumerate(tables)}
        options['0'] = "Επιστροφή"
        show_menu(options)
        
        choice = input("Επιλογή: ").strip()
        if choice == '0': break
        
        if choice in options:
            try:
                data = select_table(options[choice])
                show_table(data)
            except Exception as e:
                show_error(str(e))

def menu_admin():
    while True:
        show_header("ΣΥΣΤΗΜΑ TENNIS CLUB")
        main_options = {
            "1": "Προβολή Πινάκων",
            "2": "Αναφορές & Στατιστικά",
            "3": "Εγγραφή Μέλους σε Μάθημα",
            "4": "Συντήρηση Βάσης",
            "x": "Έξοδος"
        }
        show_menu(main_options)
        
        choice = input("Επιλογή: ").strip().lower()

        match choice :
            case 'x':
                print("Αντίο!")
                break

            case '1':
                view_tables_menu()

            case '2':
                # Υπο-μενού για αναφορές
                show_header("ΑΝΑΦΟΡΕΣ")
                print("A. Κατάσταση & Status Μελών")
                print("B. Διαθεσιμότητα Μαθημάτων")
                sub = input("Επιλογή (A/B): ").strip().upper()  
                if sub == 'A':
                    show_table(get_member_stats())
                elif sub == 'B':
                    show_table(get_lesson_availability())

            case '3':
                # Εγγραφή σε μάθημα (Insert σε 3 πίνακες)
                show_header("ΕΓΓΡΑΦΗ ΣΕ ΜΑΘΗΜΑ")
                try:
                    m_id = input("ID Μέλους: ")
                    l_id = input("ID Μαθήματος: ")
                    cost = input("Ποσό Πληρωμής: ")
                    
                    # Κλήση της συνάρτησης του Model
                    enroll_member_in_lesson(m_id, l_id, cost)
                    show_success("Η εγγραφή και η πληρωμή ολοκληρώθηκαν!")
                except Exception as e:
                    show_error(f"Η εγγραφή απέτυχε: {e}")

            case '4':
                # Cleanup
                try:
                    count = delete_orphan_payments()
                    show_success(f"Διαγράφηκαν {count} ορφανές πληρωμές.")
                except Exception as e:
                    show_error(str(e))

            case _:
                print("Αντίο!")
                break

def menu_member():
    while True:
        show_header("ΣΥΣΤΗΜΑ TENNIS CLUB")
        main_options = {
            "1": "Προβολή Πινάκων",
            "2": "Αναφορές & Στατιστικά",
            "3": "Εγγραφή Μέλους σε Μάθημα",
            "4": "Συντήρηση Βάσης",
            "x": "Έξοδος"
        }
        show_menu(main_options)
        
        choice = input("Επιλογή: ").strip().lower()

        match choice :
            case 'x':
                print("Αντίο!")
                break

            case '1':
                view_tables_menu()

            case '2':
                # Υπο-μενού για αναφορές
                show_header("ΑΝΑΦΟΡΕΣ")
                print("A. Κατάσταση & Status Μελών")
                print("B. Διαθεσιμότητα Μαθημάτων")
                sub = input("Επιλογή (A/B): ").strip().upper()  
                if sub == 'A':
                    show_table(get_member_stats())
                elif sub == 'B':
                    show_table(get_lesson_availability())

            case '3':
                # Εγγραφή σε μάθημα (Insert σε 3 πίνακες)
                show_header("ΕΓΓΡΑΦΗ ΣΕ ΜΑΘΗΜΑ")
                try:
                    m_id = input("ID Μέλους: ")
                    l_id = input("ID Μαθήματος: ")
                    cost = input("Ποσό Πληρωμής: ")
                    
                    # Κλήση της συνάρτησης του Model
                    enroll_member_in_lesson(m_id, l_id, cost)
                    show_success("Η εγγραφή και η πληρωμή ολοκληρώθηκαν!")
                except Exception as e:
                    show_error(f"Η εγγραφή απέτυχε: {e}")

            case '4':
                # Cleanup
                try:
                    count = delete_orphan_payments()
                    show_success(f"Διαγράφηκαν {count} ορφανές πληρωμές.")
                except Exception as e:
                    show_error(str(e))

            case _:
                print("Αντίο!")
                break

def admin_registration():
        password = "admin"
        while True:
            show_header("ΣΥΝΔΕΣΗ")
            user_pass = input("Εισάγεται κωδικό (ENTER για έξοδο):")
            if user_pass == password:
                menu_admin()
                break
            elif user_pass == "":
                break
            else:
                print("Λανθασμένος κωδικός")

def main():
    while True:
        show_header("ΣΥΝΔΕΣΗ")
        main_options = {
            "1": "Μέλος",
            "2": "Admin",
            "x": "Έξοδος"
        }
        show_menu(main_options)

        choice = input("Επιλογή: ").strip().lower()

        match choice:
            case '1':
                menu_member()
            
            case '2':
                admin_registration()

            case 'x':
                print("Αντίο!")
                break

            case _:
                print("Αντίο!")
                break      

if __name__ == "__main__":
    main()