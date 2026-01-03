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

def main():
    while True:
        show_header("ΣΥΣΤΗΜΑ TENNIS CLUB")
        main_options = {
            "1": "Προβολή Πινάκων (Raw Data)",
            "2": "Αναφορές & Στατιστικά (Queries 1 & 8)",
            "3": "Εγγραφή Μέλους σε Μάθημα (Query 7)",
            "4": "Συντήρηση Βάσης (Query 2)",
            "x": "Έξοδος"
        }
        show_menu(main_options)
        
        choice = input("Επιλογή: ").strip().lower()

        if choice == 'x':
            print("Αντίο!")
            break

        elif choice == '1':
            view_tables_menu()

        elif choice == '2':
            # Υπο-μενού για αναφορές
            show_header("ΑΝΑΦΟΡΕΣ")
            print("A. Κατάσταση & Status Μελών")
            print("B. Διαθεσιμότητα Μαθημάτων")
            sub = input("Επιλογή (A/B): ").strip().upper()
            
            if sub == 'A':
                show_table(get_member_stats())
            elif sub == 'B':
                show_table(get_lesson_availability())

        elif choice == '3':
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

        elif choice == '4':
            # Cleanup
            try:
                count = delete_orphan_payments()
                show_success(f"Διαγράφηκαν {count} ορφανές πληρωμές.")
            except Exception as e:
                show_error(str(e))

if __name__ == "__main__":
    main()