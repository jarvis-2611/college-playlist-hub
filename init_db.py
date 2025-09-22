import sqlite3


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the songs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            song_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            link TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            dislikes INTEGER DEFAULT 0,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create the votes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_id INTEGER NOT NULL,
            user_ip TEXT NOT NULL,
            UNIQUE(song_id, user_ip),
            FOREIGN KEY (song_id) REFERENCES songs (song_id)
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print("Database and tables created successfully!")