import psycopg2

def test_connection():
    try:
        conn = psycopg2.connect(
        host="localhost",
        dbname="phonebook",
        user="postgres",
        password="q1w2e3r4"  # В кавычках!
        )
        print("✅ Успешное подключение к базе данных!")
        conn.close()
    except Exception as e:
        print("❌ Ошибка подключения:", e)

test_connection()
