from app import engineers, rota, incidents


def get_valid_id(prompt):
    """Prompt the user for an integer ID, rejecting non-numeric input. Enter 0 to cancel."""
    while True:
        value = input(prompt + " (or 0 to go back): ").strip()
        if value == "0":
            return None
        if value.isdigit():
            return int(value)
        print("✘ Invalid input — please enter a numeric ID.")


def get_input(prompt, allow_empty=False):
    """Prompt for text input. Returns None if user enters 0 to go back."""
    value = input(prompt + " (or 0 to go back): ").strip()
    if value == "0":
        return None
    if not allow_empty and not value:
        return ""
    return value


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
            try:
                name = get_input("Name")
                if name is None:
                    continue
                if not name:
                    print("✘ Name cannot be empty.")
                    continue

                email = get_input("Email")
                if email is None:
                    continue
                if not email or "@" not in email:
                    print("✘ Please enter a valid email address.")
                    continue

                phone = get_input("Phone (optional, press Enter to skip)", allow_empty=True)
                if phone is None:
                    continue
                phone = phone or None

                engineers.add_engineer(name, email, phone)
                print(f"✔ Engineer '{name}' added successfully.")
            except Exception as e:
                print(f"✘ Could not add engineer: {e}")

        elif choice == "2":
            try:
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
            except Exception as e:
                print(f"✘ Could not retrieve engineers: {e}")

        elif choice == "3":
            try:
                term = get_input("Search by name")
                if term is None:
                    continue
                if not term:
                    print("✘ Please enter a search term.")
                    continue
                results = engineers.search_engineers_by_name(term)
                if not results:
                    print("No engineers found matching that name.")
                else:
                    for eng in results:
                        print(f"  [{eng['id']}] {eng['name']} - {eng['email']}")
            except Exception as e:
                print(f"✘ Search failed: {e}")

        elif choice == "4":
            try:
                engineer_id = get_valid_id("Enter Engineer ID to update")
                if engineer_id is None:
                    continue

                existing = engineers.get_engineer_by_id(engineer_id)
                if not existing:
                    print("✘ No engineer found with that ID.")
                    continue

                print(f"\nCurrent details for '{existing['name']}':")
                print(f"  Name:  {existing['name']}")
                print(f"  Email: {existing['email']}")
                print(f"  Phone: {existing['phone'] or 'N/A'}")
                print("\nPress Enter to keep the current value. Enter 0 at any point to go back.\n")

                name = input(f"Name [{existing['name']}] (or 0 to go back): ").strip()
                if name == "0":
                    continue
                name = name or existing['name']

                email = input(f"Email [{existing['email']}] (or 0 to go back): ").strip()
                if email == "0":
                    continue
                email = email or existing['email']
                if "@" not in email:
                    print("✘ Invalid email address.")
                    continue

                phone_input = input(f"Phone [{existing['phone'] or 'N/A'}] (or 0 to go back): ").strip()
                if phone_input == "0":
                    continue
                phone = phone_input if phone_input else existing['phone']

                engineers.update_engineer(engineer_id, name, email, phone)
                print("✔ Engineer updated successfully.")
            except Exception as e:
                print(f"✘ Could not update engineer: {e}")

        elif choice == "5":
            try:
                engineer_id = get_valid_id("Enter Engineer ID to delete")
                if engineer_id is None:
                    continue

                existing = engineers.get_engineer_by_id(engineer_id)
                if not existing:
                    print("✘ No engineer found with that ID.")
                    continue

                confirm = input(f"Are you sure you want to delete '{existing['name']}'? (yes/no): ").strip().lower()
                if confirm == "yes":
                    engineers.delete_engineer(engineer_id)
                    print("✔ Engineer deleted successfully.")
                else:
                    print("Deletion cancelled.")
            except Exception as e:
                print(f"✘ Could not delete engineer: {e}")

        elif choice == "0":
            break
        else:
            print("✘ Invalid choice, please try again.")


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
            try:
                engineer_id = get_valid_id("Engineer ID")
                if engineer_id is None:
                    continue

                existing = engineers.get_engineer_by_id(engineer_id)
                if not existing:
                    print("✘ No engineer found with that ID.")
                    continue

                start_date = get_input("Start Date (YYYY-MM-DD)")
                if start_date is None:
                    continue
                if not start_date:
                    print("✘ Start date cannot be empty.")
                    continue

                end_date = get_input("End Date (YYYY-MM-DD)")
                if end_date is None:
                    continue
                if not end_date:
                    print("✘ End date cannot be empty.")
                    continue

                if end_date < start_date:
                    print("✘ End date cannot be before start date.")
                    continue

                shift = get_input("Shift (day/night)")
                if shift is None:
                    continue
                if shift.lower() not in ("day", "night"):
                    print("✘ Shift must be either 'day' or 'night'.")
                    continue

                rota.assign_rota(engineer_id, start_date, end_date, shift.lower())
                print("✔ Rota entry added successfully.")
            except Exception as e:
                print(f"✘ Could not add rota entry: {e}")

        elif choice == "2":
            try:
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
            except Exception as e:
                print(f"✘ Could not retrieve rota: {e}")

        elif choice == "3":
            try:
                query_date = get_input("Enter date to check (YYYY-MM-DD)")
                if query_date is None:
                    continue
                if not query_date:
                    print("✘ Date cannot be empty.")
                    continue
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
            except Exception as e:
                print(f"✘ Could not query rota: {e}")

        elif choice == "4":
            try:
                engineer_id = get_valid_id("Enter Engineer ID")
                if engineer_id is None:
                    continue

                existing = engineers.get_engineer_by_id(engineer_id)
                if not existing:
                    print("✘ No engineer found with that ID.")
                    continue

                results = rota.get_rota_by_engineer(engineer_id)
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
            except Exception as e:
                print(f"✘ Could not retrieve rota for engineer: {e}")

        elif choice == "5":
            try:
                rota_id = get_valid_id("Enter Rota ID to delete")
                if rota_id is None:
                    continue

                confirm = input(f"Are you sure you want to delete rota entry {rota_id}? (yes/no): ").strip().lower()
                if confirm == "yes":
                    rota.delete_rota_entry(rota_id)
                    print("✔ Rota entry deleted successfully.")
                else:
                    print("Deletion cancelled.")
            except Exception as e:
                print(f"✘ Could not delete rota entry: {e}")

        elif choice == "0":
            break
        else:
            print("✘ Invalid choice, please try again.")


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
            try:
                rota_id = get_valid_id("Rota ID (links incident to on-call shift)")
                if rota_id is None:
                    continue

                title = get_input("Incident Title")
                if title is None:
                    continue
                if not title:
                    print("✘ Incident title cannot be empty.")
                    continue

                severity = get_input("Severity (low/medium/high/critical)")
                if severity is None:
                    continue
                if severity.lower() not in ("low", "medium", "high", "critical"):
                    print("✘ Severity must be one of: low, medium, high, critical.")
                    continue

                description = get_input("Description (optional, press Enter to skip)", allow_empty=True)
                if description is None:
                    continue
                description = description or None

                incidents.log_incident(rota_id, title, severity.lower(), description)
                print("✔ Incident logged successfully.")
            except Exception as e:
                print(f"✘ Could not log incident: {e}")

        elif choice == "2":
            try:
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
            except Exception as e:
                print(f"✘ Could not retrieve incidents: {e}")

        elif choice == "3":
            try:
                severity = get_input("Enter severity (low/medium/high/critical)")
                if severity is None:
                    continue
                if severity.lower() not in ("low", "medium", "high", "critical"):
                    print("✘ Severity must be one of: low, medium, high, critical.")
                    continue
                results = incidents.get_incidents_by_severity(severity.lower())
                if not results:
                    print("No incidents found for that severity.")
                else:
                    for inc in results:
                        resolved = "Yes" if inc["resolved"] else "No"
                        print(f"  [{inc['id']}] {inc['title']} | {inc['severity']} | {inc['raised_at']} | Resolved: {resolved}")
            except Exception as e:
                print(f"✘ Could not filter incidents: {e}")

        elif choice == "4":
            try:
                all_incidents = incidents.get_all_incidents()
                sorted_incidents = incidents.sort_incidents_by_severity(all_incidents)
                if not sorted_incidents:
                    print("No incidents found.")
                else:
                    print("\nIncidents sorted by severity (critical → low):")
                    print("\n{:<5} {:<20} {:<30} {:<10}".format("ID", "Engineer", "Title", "Severity"))
                    print("-" * 65)
                    for inc in sorted_incidents:
                        print("{:<5} {:<20} {:<30} {:<10}".format(
                            inc["id"], inc["name"], inc["title"], inc["severity"]
                        ))
            except Exception as e:
                print(f"✘ Could not sort incidents: {e}")

        elif choice == "5":
            try:
                incident_id = get_valid_id("Enter Incident ID to resolve")
                if incident_id is None:
                    continue
                incidents.resolve_incident(incident_id)
                print("✔ Incident marked as resolved.")
            except Exception as e:
                print(f"✘ Could not resolve incident: {e}")

        elif choice == "0":
            break
        else:
            print("✘ Invalid choice, please try again.")