from app import engineers, rota, incidents


def display_menu():
    """Display the main menu options."""
    print("\n========================================")
    print("       On-Call Rota Manager")
    print("========================================")
    print("1. Engineer Management")
    print("2. Rota Management")
    print("3. Incident Management")
    print("0. Exit")
    print("========================================")


def engineer_menu():
    """Display and handle the engineer management submenu."""
    while True:
        print("\n--- Engineer Management ---")
        print("1. Add Engineer")
        print("2. View All Engineers")
        print("3. Search Engineer by Name")
        print("4. Update Engineer")
        print("5. Delete Engineer")
        print("0. Back to Main Menu")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone (optional, press Enter to skip): ").strip() or None
            engineers.add_engineer(name, email, phone)
            print(f"✔ Engineer '{name}' added successfully.")

        elif choice == "2":
            all_engineers = engineers.get_all_engineers()
            if not all_engineers:
                print("No engineers found.")
            else:
                print("\n{:<5} {:<25} {:<30} {:<15}".format("ID", "Name", "Email", "Phone"))
                print("-" * 75)
                for eng in all_engineers:
                    print("{:<5} {:<25} {:<30} {:<15}".format(
                        eng["id"], eng["name"], eng["email"], eng["phone"] or "N/A"
                    ))

        elif choice == "3":
            term = input("Search by name: ").strip()
            results = engineers.search_engineers_by_name(term)
            if not results:
                print("No engineers found.")
            else:
                for eng in results:
                    print(f"  [{eng['id']}] {eng['name']} - {eng['email']}")

        elif choice == "4":
            engineer_id = input("Enter Engineer ID to update: ").strip()
            existing = engineers.get_engineer_by_id(int(engineer_id))
            if not existing:
                print("Engineer not found.")
                continue

            print(f"\nCurrent details for '{existing['name']}':")
            print(f"  Name:  {existing['name']}")
            print(f"  Email: {existing['email']}")
            print(f"  Phone: {existing['phone'] or 'N/A'}")
            print("\nPress Enter to keep the current value for any field.\n")

            name = input(f"Name [{existing['name']}]: ").strip() or existing['name']
            email = input(f"Email [{existing['email']}]: ").strip() or existing['email']
            phone_input = input(f"Phone [{existing['phone'] or 'N/A'}]: ").strip()
            phone = phone_input if phone_input else existing['phone']

            engineers.update_engineer(int(engineer_id), name, email, phone)
            print("✔ Engineer updated successfully.")

        elif choice == "5":
            engineer_id = input("Enter Engineer ID to delete: ").strip()
            engineers.delete_engineer(int(engineer_id))
            print("✔ Engineer deleted successfully.")

        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")


def rota_menu():
    """Display and handle the rota management submenu."""
    while True:
        print("\n--- Rota Management ---")
        print("1. Assign Engineer to On-Call Slot")
        print("2. View Full Rota")
        print("3. Who is On-Call for a Specific Date?")
        print("4. View Rota by Engineer")
        print("5. Delete Rota Entry")
        print("0. Back to Main Menu")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            engineer_id = input("Engineer ID: ").strip()
            start_date = input("Start Date (YYYY-MM-DD): ").strip()
            end_date = input("End Date (YYYY-MM-DD): ").strip()
            shift = input("Shift (day/night): ").strip().lower()
            rota.assign_rota(int(engineer_id), start_date, end_date, shift)
            print("✔ Rota entry added successfully.")

        elif choice == "2":
            full_rota = rota.get_full_rota()
            if not full_rota:
                print("No rota entries found.")
            else:
                print("\n{:<5} {:<25} {:<12} {:<12} {:<10}".format(
                    "ID", "Engineer", "Start Date", "End Date", "Shift"
                ))
                print("-" * 64)
                for entry in full_rota:
                    print("{:<5} {:<25} {:<12} {:<12} {:<10}".format(
                        entry["id"], entry["name"],
                        entry["start_date"], entry["end_date"], entry["shift"]
                    ))

        elif choice == "3":
            query_date = input("Enter date to check (YYYY-MM-DD): ").strip()
            results = rota.get_rota_by_date(query_date)
            if not results:
                print(f"No one is on-call for {query_date}.")
            else:
                print(f"\nOn-call engineer(s) for {query_date}:")
                print("{:<5} {:<25} {:<12} {:<12} {:<10}".format(
                    "ID", "Engineer", "Start Date", "End Date", "Shift"
                ))
                print("-" * 64)
                for entry in results:
                    print("{:<5} {:<25} {:<12} {:<12} {:<10}".format(
                        entry["id"], entry["name"],
                        entry["start_date"], entry["end_date"], entry["shift"]
                    ))

        elif choice == "4":
            engineer_id = input("Enter Engineer ID: ").strip()
            results = rota.get_rota_by_engineer(int(engineer_id))
            if not results:
                print("No rota entries found for that engineer.")
            else:
                print("\n{:<5} {:<25} {:<12} {:<12} {:<10}".format(
                    "ID", "Engineer", "Start Date", "End Date", "Shift"
                ))
                print("-" * 64)
                for entry in results:
                    print("{:<5} {:<25} {:<12} {:<12} {:<10}".format(
                        entry["id"], entry["name"],
                        entry["start_date"], entry["end_date"], entry["shift"]
                    ))

        elif choice == "5":
            rota_id = input("Enter Rota ID to delete: ").strip()
            rota.delete_rota_entry(int(rota_id))
            print("✔ Rota entry deleted successfully.")

        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")


def incident_menu():
    """Display and handle the incident management submenu."""
    while True:
        print("\n--- Incident Management ---")
        print("1. Log New Incident")
        print("2. View All Incidents")
        print("3. Filter Incidents by Severity")
        print("4. View Incidents Sorted by Severity")
        print("5. Resolve Incident")
        print("0. Back to Main Menu")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            rota_id = input("Rota ID (links incident to on-call shift): ").strip()
            title = input("Incident Title: ").strip()
            severity = input("Severity (low/medium/high/critical): ").strip().lower()
            description = input("Description (optional, press Enter to skip): ").strip() or None
            incidents.log_incident(int(rota_id), title, severity, description)
            print("✔ Incident logged successfully.")

        elif choice == "2":
            all_incidents = incidents.get_all_incidents()
            if not all_incidents:
                print("No incidents found.")
            else:
                print("\n{:<5} {:<20} {:<30} {:<10} {:<20} {:<10}".format(
                    "ID", "Engineer", "Title", "Severity", "Raised At", "Resolved"
                ))
                print("-" * 95)
                for inc in all_incidents:
                    resolved = "Yes" if inc["resolved"] else "No"
                    print("{:<5} {:<20} {:<30} {:<10} {:<20} {:<10}".format(
                        inc["id"], inc["name"], inc["title"],
                        inc["severity"], inc["raised_at"], resolved
                    ))

        elif choice == "3":
            severity = input("Enter severity to filter by (low/medium/high/critical): ").strip().lower()
            results = incidents.get_incidents_by_severity(severity)
            if not results:
                print("No incidents found for that severity.")
            else:
                for inc in results:
                    resolved = "Yes" if inc["resolved"] else "No"
                    print(f"  [{inc['id']}] {inc['title']} | {inc['severity']} | {inc['raised_at']} | Resolved: {resolved}")

        elif choice == "4":
            all_incidents = incidents.get_all_incidents()
            sorted_incidents = incidents.sort_incidents_by_severity(all_incidents)
            if not sorted_incidents:
                print("No incidents found.")
            else:
                print("\nIncidents sorted by severity (critical → low):")
                for inc in sorted_incidents:
                    print(f"  [{inc['id']}] {inc['title']} | {inc['severity']} | {inc['name']}")

        elif choice == "5":
            incident_id = input("Enter Incident ID to resolve: ").strip()
            incidents.resolve_incident(int(incident_id))
            print("✔ Incident marked as resolved.")

        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")
