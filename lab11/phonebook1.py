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
            cur.execute("CALL insert_or_update_user(%s, %s);", (name, phone))
    print("Contact inserted or updated!")

def import_from_csv(file_path):
    with get_connection() as conn:
        with conn.cursor() as cur:
            with open(file_path, newline='', encoding='utf-8') as file:
                rows = csv.reader(file)
                names = []
                phones = []
                for entry in rows:
                    names.append(entry[0])
                    phones.append(entry[1])
                cur.execute("CALL insert_many_users(%s, %s, NULL);", (names, phones))
    print("CSV import complete!")

def update_contact():
    name = input("Enter the name of the contact to update: ")
    phone = input("Enter new phone number: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL insert_or_update_user(%s, %s);", (name, phone))
    print("Contact updated!")

def view_all():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM paginate_users(1000, 0);")
            contacts = cur.fetchall()
            for contact in contacts:
                print(f"ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}")

def search_contact():
    pattern = input("Enter name or number pattern to search: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_pattern(%s);", (pattern,))
            result = cur.fetchall()
            for row in result:
                print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")

def delete_contact():
    value = input("Enter name or phone to delete: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_user(%s);", (value,))
    print("Contact deleted!")

def main():
    while True:
        print("\n📱 Phonebook Menu")
        print("1. Add or update contact")
        print("2. Import contacts from CSV")
        print("3. Update contact phone")
        print("4. View all contacts")
        print("5. Search contact by name or phone")
        print("6. Delete contact by name or phone")
        print("7. Exit")

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
            delete_contact()
        elif choice == '7':
            break
        else:
            print("Invalid input, please try again.")

if __name__ == '__main__':
    main()
