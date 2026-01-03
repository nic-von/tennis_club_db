def show_header(title):
    print("\n" + "=" * 60)
    print(f"   {title.upper()}")
    print("=" * 60)

def show_table(data):
    if not data:
        print(" [!] Δεν βρέθηκαν δεδομένα.")
        return

    headers = list(data[0].keys())
    col_widths = {h: max(len(h), max(len(str(r[h])) for r in data)) for h in headers}
    
    header_row = " | ".join(h.ljust(col_widths[h]) for h in headers)
    print(header_row)
    print("-" * len(header_row))

    for row in data:
        values = [str(row[h]).ljust(col_widths[h]) for h in headers]
        print(" | ".join(values))
    print("\n")

def show_member_details(member):
    print(f"\n--- ΚΑΡΤΕΛΑ ΜΕΛΟΥΣ [ID: {member['member_id']}] ---")
    print(f"Όνομα:      {member['first_name']} {member['last_name']}")
    print(f"Τηλέφωνο:   {member['phone']}")
    print(f"Email:      {member['mail']}")
    print(f"Διεύθυνση:  {member['address']}")
    print(f"Ημ. Γένν.:  {member['date_of_birth']}")
    print("-" * 40)

def show_tournaments(data):
    """Ειδική προβολή για Τουρνουά."""
    if not data:
        print(" [!] Δεν υπάρχουν επερχόμενα τουρνουά.")
        return
    print(f"\n{'ID':<4} | {'ΟΝΟΜΑ':<30} | {'ΚΑΤΗΓΟΡΙΑ':<15} | {'ΕΝΑΡΞΗ':<12}")
    print("-" * 70)
    for row in data:
        print(f"{row['tournament_id']:<4} | {row['name']:<30} | {row['category']:<15} | {row['start_date']:<12}")
    print("\n")

def show_schedule(schedule_data):
    if not schedule_data:
        print(" [!] Το πρόγραμμα είναι κενό για τα κριτήρια που επιλέξατε.")
        return
    
    print(f"\n{'ΓΗΠΕΔΟ':<8} | {'ΔΡΑΣΤΗΡΙΟΤΗΤΑ':<20} | {'ΕΝΑΡΞΗ':<20} | {'ΛΗΞΗ':<20} | {'ΛΕΠΤΟΜΕΡΕΙΕΣ'}")
    print("-" * 110)
    for row in schedule_data:
        court = row.get('court_id', '-')
        activity = row.get('Activity', row.get('activity', '-'))
        start = row.get('start_datetime', '-')
        end = row.get('end_datetime', '-')
        details = row.get('Details', row.get('description', '-'))
        
        print(f"{str(court):<8} | {str(activity):<20} | {str(start):<20} | {str(end):<20} | {str(details)}")
    print("\n")

def show_stats(stats):
    print("\n--- ΟΙΚΟΝΟΜΙΚΑ ΣΤΑΤΙΣΤΙΚΑ ---")
    print(f"Συνολικά Μέλη:    {stats['total_members']}")
    print(f"Συνολικά Έσοδα:   {stats['total_revenue']} €")
    print("-" * 30)

def show_menu(options):
    print("\n--- MENOY ΕΠΙΛΟΓΩΝ ---")
    for key, text in options.items():
        print(f"[{key}] {text}")
    print("-" * 22)

def show_success(msg):
    print(f" [OK] {msg}")

def show_error(msg):
    print(f" [X] ΣΦΑΛΜΑ: {msg}")