import psycopg2
import csv

def get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="phonebook",
        user="postgres",
        password="q1w2e3r4"
    )

def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    print("Contact added!")

def import_from_csv(file_path):
    with get_connection() as conn:
        with conn.cursor() as cur:
            with open(file_path, newline='', encoding='utf-8') as file:
                rows = csv.reader(file)
                for entry in rows:
                    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (entry[0], entry[1]))
    print("CSV import complete!")

def update_contact():
    name = input("Enter the name of the contact to update: ")
    new_phone = input("Enter new phone number: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
    print("Contact updated!")

def view_all():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook")
            contacts = cur.fetchall()
            for contact in contacts:
                print(contact)

def search_contact():
    name = input("Enter name to search: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
            result = cur.fetchall()
            print(result)

def search_by_phone():
    phone = input("Enter phone to search: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
            result = cur.fetchall()
            print(result)

def delete_contact():
    name = input("Enter name to delete: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    print("Contact deleted by name!")

def delete_by_phone():
    phone = input("Enter phone number to delete: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    print("Contact deleted by phone!")

def main():
    while True:
        print("\n📱 Phonebook Menu")
        print("1. Add contact manually")
        print("2. Import contacts from CSV")
        print("3. Update contact phone")
        print("4. View all contacts")
        print("5. Search contact by name")
        print("6. Search contact by phone")
        print("7. Delete contact by name")
        print("8. Delete contact by phone")
        print("9. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_contact()
        elif choice == '2':
            import_from_csv(input("Enter CSV file path: "))
        elif choice == '3':
            update_contact()
        elif choice == '4':
            view_all()
        elif choice == '5':
            search_contact()
        elif choice == '6':
            search_by_phone()
        elif choice == '7':
            delete_contact()
        elif choice == '8':
            delete_by_phone()
        elif choice == '9':
            break
        else:
            print("Invalid input, please try again.")

if __name__ == '__main__':
    main()
