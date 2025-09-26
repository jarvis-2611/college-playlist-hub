import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    # This SQL command adds the 'created_at' column to the existing songs table.
    cursor.execute('ALTER TABLE songs ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP')
    print("Successfully added 'created_at' column.")
except sqlite3.OperationalError as e:
    print(f"Error: {e}. The column likely already exists.")

conn.commit()
conn.close()