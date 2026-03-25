import sqlite3
import pprint

try:
    conn = sqlite3.connect('reflecta.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    
    if not users:
        print("No users found in the database. You can just register a new account.")
    else:
        print("--- Registered Users ---")
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")
            
    conn.close()
except Exception as e:
    print(f"Error reading database: {e}")
