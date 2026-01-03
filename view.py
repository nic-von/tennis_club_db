def show_header(title):
    print("\n" + "=" * 50)
    print(f"   {title.upper()}")
    print("=" * 50)

def show_table(data):
    if not data:
        print(" [!] Δεν βρέθηκαν δεδομένα.")
        return

    headers = list(data[0].keys())
    
    # Υπολογισμός πλάτους στηλών για ωραία στοίχιση
    col_widths = {h: max(len(h), max(len(str(r[h])) for r in data)) for h in headers}
    
    # Εκτύπωση Header
    header_row = " | ".join(h.ljust(col_widths[h]) for h in headers)
    print(header_row)
    print("-" * len(header_row))

    # Εκτύπωση Rows
    for row in data:
        values = [str(row[h]).ljust(col_widths[h]) for h in headers]
        print(" | ".join(values))
    print("\n")

def show_menu(options):
    print("\n--- MENOY ΕΠΙΛΟΓΩΝ ---")
    for key, text in options.items():
        print(f"[{key}] {text}")
    print("----------------------")

def show_success(msg):
    print(f" [OK] {msg}")

def show_error(msg):
    print(f" [X] ΣΦΑΛΜΑ: {msg}")