from app.database import initialise_db
from app.menu import display_menu, engineer_menu, rota_menu, incident_menu


def main():
    """Main entry point for the On-Call Rota Manager."""
    initialise_db()
    print("Database initialised successfully.")

    while True:
        display_menu()
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            engineer_menu()
        elif choice == "2":
            rota_menu()
        elif choice == "3":
            incident_menu()
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
