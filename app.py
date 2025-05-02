import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# Load environment variables from .env (SECRET_KEY, DATABASE, etc.)
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change_this_in_production')

# Database file path (can be overridden via env var)
DATABASE = os.getenv('DATABASE', 'holiday_club.db')


def get_db_connection():
    """Create a new database connection with foreign keys enabled."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn


def init_db():
    """Initialize the database tables: users and stories."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            location TEXT NOT NULL,
            story_text TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')
    conn.commit()
    conn.close()


def seed_data():
    """
    Seed a default user and sample stories linked to that user.
    This runs once if tables are empty.
    """
    conn = get_db_connection()

    # 1) Ensure a default user exists
    user = conn.execute(
        "SELECT id FROM users WHERE username = ?",
        ("default_user",)
    ).fetchone()

    if user is None:
        conn.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            ("default_user", "user@example.com")
        )
        conn.commit()
        user = conn.execute(
            "SELECT id FROM users WHERE username = ?",
            ("default_user",)
        ).fetchone()

    user_id = user['id']

    # 2) Seed sample stories for that user if none exist
    count = conn.execute(
        "SELECT COUNT(*) AS c FROM stories WHERE user_id = ?",
        (user_id,)
    ).fetchone()['c']

    if count == 0:
        sample_stories = [
            (user_id, "Paris, France",
             "I visited the Eiffel Tower and enjoyed croissants by the Seine."),
            (user_id, "Tokyo, Japan",
             "I tried sushi at Tsukiji market and explored Shibuya Crossing."),
            (user_id, "Cairo, Egypt",
             "Saw the pyramids at Giza and experienced the local markets."),
            (user_id, "New York, USA",
             "Loved the hustle of Times Square and a stroll in Central Park."),
            (user_id, "Sydney, Australia",
             "Visited the Opera House and enjoyed Bondi Beach.")
        ]
        for uid, loc, txt in sample_stories:
            conn.execute(
                "INSERT INTO stories (user_id, location, story_text) VALUES (?, ?, ?)",
                (uid, loc, txt)
            )
        conn.commit()

    conn.close()


# -------------------
# ROUTE HANDLERS
# -------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Collect contact form fields
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Flash acknowledgement
        flash("Thank you for your message. We'll get back to you soon!", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html')


@app.route('/viewstory')
def view_story():
    conn = get_db_connection()
    stories = conn.execute('''
        SELECT s.id, s.location, s.story_text, u.username
          FROM stories s
          JOIN users u ON s.user_id = u.id
         ORDER BY s.id DESC
    ''').fetchall()
    conn.close()
    return render_template('viewstory.html', stories=stories)


@app.route('/story/<int:story_id>')
def story_detail(story_id):
    conn = get_db_connection()
    story = conn.execute('''
        SELECT s.id, s.location, s.story_text, u.username
          FROM stories s
          JOIN users u ON s.user_id = u.id
         WHERE s.id = ?
    ''', (story_id,)).fetchone()
    conn.close()

    if story is None:
        flash("Story not found!", "error")
        return redirect(url_for('view_story'))

    return render_template('story.html', story=story)


@app.route('/addstory', methods=['GET', 'POST'])
def add_story():
    if request.method == 'POST':
        location   = request.form.get('location')
        story_text = request.form.get('story_text')

        if not location or not story_text:
            flash("Please provide both location and story text.", "error")
            return redirect(url_for('add_story'))

        # All new stories by default_user (id=1)
        user_id = 1

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO stories (user_id, location, story_text)
                 VALUES (?, ?, ?)
        ''', (user_id, location, story_text))
        conn.commit()
        conn.close()

        flash("Story added successfully!", "success")
        return redirect(url_for('view_story'))

    return render_template('addstory.html')


@app.route('/editstory/<int:story_id>', methods=['GET', 'POST'])
def edit_story(story_id):
    conn = get_db_connection()
    story = conn.execute(
        'SELECT * FROM stories WHERE id = ?',
        (story_id,)
    ).fetchone()

    if story is None:
        conn.close()
        flash("Story not found!", "error")
        return redirect(url_for('view_story'))

    if request.method == 'POST':
        location   = request.form.get('location')
        story_text = request.form.get('story_text')

        if not location or not story_text:
            flash("Please fill out all fields.", "error")
            return redirect(url_for('edit_story', story_id=story_id))

        conn.execute('''
            UPDATE stories
               SET location = ?, story_text = ?
             WHERE id = ?
        ''', (location, story_text, story_id))
        conn.commit()
        conn.close()

        flash("Story updated successfully!", "success")
        return redirect(url_for('view_story'))

    conn.close()
    return render_template('editstory.html', story=story)


@app.route('/deletestory/<int:story_id>', methods=['GET', 'POST'])
def delete_story(story_id):
    conn = get_db_connection()
    story = conn.execute(
        'SELECT * FROM stories WHERE id = ?',
        (story_id,)
    ).fetchone()

    if story is None:
        conn.close()
        flash("Story not found!", "error")
        return redirect(url_for('view_story'))

    if request.method == 'POST':
        conn.execute('DELETE FROM stories WHERE id = ?', (story_id,))
        conn.commit()
        conn.close()
        flash("Story deleted successfully!", "success")
        return redirect(url_for('view_story'))

    conn.close()
    return render_template('deletestory.html', story=story)


# -------------------
# MAIN EXECUTION
# -------------------

if __name__ == '__main__':
    # Create tables and seed initial data
    init_db()
    seed_data()
    # Run the app (debug=False for production)
    app.run(debug=False)
