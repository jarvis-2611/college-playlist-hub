from flask import Flask, render_template, request, redirect, url_for,flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn


# Home page: Displays the top trending songs and the submission form
@app.route('/')
def index():
    conn = get_db_connection()
    # Query to get songs, ordered by the difference between likes and dislikes
    songs = conn.execute('SELECT * FROM songs ORDER BY (likes - dislikes) DESC').fetchall()
    conn.close()
    return render_template('index.html', songs=songs)


# Handles the form submission for adding a new song
@app.route('/add_song', methods=['POST'])
def add_song():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        link = request.form['link']

        conn = get_db_connection()
        conn.execute('INSERT INTO songs (title, artist, link) VALUES (?, ?, ?)',
                     (title, artist, link))
        conn.commit()
        conn.close()
        flash('Song added successfully!', 'success')
        return redirect(url_for('index'))


# Handles the voting for a song (like or dislike)
@app.route('/vote/<int:song_id>/<vote_type>', methods=['POST'])
def vote(song_id, vote_type):
    conn = get_db_connection()
    user_ip = request.remote_addr  # Get the user's IP to prevent multiple votes

    # Check if the user has already voted on this song
    existing_vote = conn.execute('SELECT * FROM votes WHERE song_id = ? AND user_ip = ?', (song_id, user_ip)).fetchone()

    if not existing_vote:
        # Update the song's vote count
        if vote_type == 'like':
            conn.execute('UPDATE songs SET likes = likes + 1 WHERE song_id = ?', (song_id,))
        elif vote_type == 'dislike':
            conn.execute('UPDATE songs SET dislikes = dislikes + 1 WHERE song_id = ?', (song_id,))

        # Record the vote in the votes table
        conn.execute('INSERT INTO votes (song_id, user_ip) VALUES (?, ?)', (song_id, user_ip))
        conn.commit()
        flash('Your vote has been counted!', 'success')
    else:
        flash('You have already voted on this song.', 'error')
    conn.close()
    return redirect(url_for('index'))
@app.route('/search')
def search():
    conn = get_db_connection()
    query = request.args.get('query', '')

    # Use the LIKE operator for partial matching on title or artist
    # The % is a wildcard character in SQL
    songs = conn.execute(
        'SELECT * FROM songs WHERE title LIKE ? OR artist LIKE ? ORDER BY (likes - dislikes) DESC',
        ('%' + query + '%', '%' + query + '%')
    ).fetchall()

    conn.close()

    return render_template('index.html', songs=songs, search_query=query)
if __name__ == '__main__':
    app.run(debug=True)