import os
import sqlite3
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, g
)
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Load environment variables from .env
load_dotenv()

# ----- App Configuration -----
app = Flask(__name__)

# Require a real SECRET_KEY in all environments
secret = os.getenv('SECRET_KEY')
if not secret:
    raise RuntimeError("SECRET_KEY environment variable is required")
app.config['SECRET_KEY'] = secret

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_PERMANENT'] = False

# Path to SQLite DB 
DATABASE = os.getenv('DATABASE', 'holiday_club.db')


# ----- Database Helpers -----
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    # ensure foreign keys are enforced
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn


def init_db():
    """Create users and stories tables if they don’t exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password_hash TEXT NOT NULL
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
    Seed a default user and some sample stories if the DB is empty.
    This uses INSERT OR IGNORE so that concurrent workers
    don’t both crash trying to insert the same username.
    """
    conn = get_db_connection()

    # 1) Ensure default_user exists 
    conn.execute(
        "INSERT OR IGNORE INTO users (username, email, password_hash) "
        "VALUES (?, ?, ?)",
        ("default_user", "user@example.com", generate_password_hash("password"))
    )
    conn.commit()

    # fetch its id now that we’ve guaranteed it’s there
    user = conn.execute(
        "SELECT id FROM users WHERE username = ?",
        ("default_user",)
    ).fetchone()
    user_id = user["id"]

    # 2) Seed sample stories for that user if none yet exist
    count = conn.execute(
        "SELECT COUNT(*) AS c FROM stories WHERE user_id = ?",
        (user_id,)
    ).fetchone()["c"]

    if count == 0:
        sample_stories = [
            (user_id, "Paris, France",  "I visited the Eiffel Tower and enjoyed croissants by the Seine."),
            (user_id, "Tokyo, Japan",   "I tried sushi at Tsukiji market and explored Shibuya Crossing."),
            (user_id, "Cairo, Egypt",   "Saw the pyramids at Giza and experienced the local markets."),
            (user_id, "New York, USA",  "Loved the hustle of Times Square and a stroll in Central Park."),
            (user_id, "Sydney, Australia", "Visited the Opera House and enjoyed Bondi Beach.")
        ]
        # again use OR IGNORE just to be safe if two workers race here too
        for uid, loc, txt in sample_stories:
            conn.execute(
                "INSERT OR IGNORE INTO stories (user_id, location, story_text) VALUES (?, ?, ?)",
                (uid, loc, txt)
            )
        conn.commit()

    conn.close()



# ----- Immediately ensure DB is initialized & seeded on startup -----
init_db()
seed_data()


# ----- Authentication Helpers -----
def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in first.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapped


@app.before_request
def load_logged_in_user():
    """Load user object into g.user if logged in."""
    user_id = session.get('user_id')
    g.user = None
    if user_id:
        conn = get_db_connection()
        g.user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        conn.close()


# ----- Authentication Routes -----
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        email = request.form['email']
        pwd   = request.form['password']
        if not uname or not email or not pwd:
            flash("All fields are required.", "error")
            return redirect(url_for('register'))

        conn = get_db_connection()
        existing = conn.execute(
            "SELECT id FROM users WHERE username = ?", (uname,)
        ).fetchone()
        if existing:
            flash("Username already taken.", "error")
            conn.close()
            return redirect(url_for('register'))

        pw_hash = generate_password_hash(pwd)
        conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (uname, email, pw_hash)
        )
        conn.commit()
        conn.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd   = request.form['password']
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (uname,)
        ).fetchone()
        conn.close()
        if user and check_password_hash(user['password_hash'], pwd):
            session.clear()
            session['user_id'] = user['id']
            flash(f"Welcome, {user['username']}!", "success")
            return redirect(url_for('index'))
        flash("Invalid credentials.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("You’ve been logged out.", "success")
    return redirect(url_for('index'))


# ----- Main Routes -----
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
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
@login_required
def add_story():
    if request.method == 'POST':
        loc = request.form['location']
        txt = request.form['story_text']
        if not loc or not txt:
            flash("Please fill in all fields.", "error")
            return redirect(url_for('add_story'))

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO stories (user_id, location, story_text) VALUES (?, ?, ?)",
            (g.user['id'], loc, txt)
        )
        conn.commit()
        conn.close()

        flash("Story added successfully!", "success")
        return redirect(url_for('view_story'))

    return render_template('addstory.html')


@app.route('/editstory/<int:story_id>', methods=['GET', 'POST'])
@login_required
def edit_story(story_id):
    conn = get_db_connection()
    story = conn.execute(
        'SELECT * FROM stories WHERE id = ?', (story_id,)
    ).fetchone()

    if story is None:
        conn.close()
        flash("Story not found!", "error")
        return redirect(url_for('view_story'))

    if story['user_id'] != g.user['id']:
        conn.close()
        flash("You can only modify your own stories.", "error")
        return redirect(url_for('view_story'))

    if request.method == 'POST':
        loc = request.form['location']
        txt = request.form['story_text']
        if not loc or not txt:
            flash("Please fill out all fields.", "error")
            return redirect(url_for('edit_story', story_id=story_id))

        conn.execute('''
            UPDATE stories
               SET location = ?, story_text = ?
             WHERE id = ?
        ''', (loc, txt, story_id))
        conn.commit()
        conn.close()

        flash("Story updated successfully!", "success")
        return redirect(url_for('view_story'))

    conn.close()
    return render_template('editstory.html', story=story)


@app.route('/deletestory/<int:story_id>', methods=['GET', 'POST'])
@login_required
def delete_story(story_id):
    conn = get_db_connection()
    story = conn.execute(
        'SELECT * FROM stories WHERE id = ?', (story_id,)
    ).fetchone()

    if story is None:
        conn.close()
        flash("Story not found!", "error")
        return redirect(url_for('view_story'))

    if story['user_id'] != g.user['id']:
        conn.close()
        flash("You can only delete your own stories.", "error")
        return redirect(url_for('view_story'))

    if request.method == 'POST':
        conn.execute('DELETE FROM stories WHERE id = ?', (story_id,))
        conn.commit()
        conn.close()
        flash("Story deleted successfully!", "success")
        return redirect(url_for('view_story'))

    conn.close()
    return render_template('deletestory.html', story=story)


# ----- Main Execution (dev only) -----
if __name__ == '__main__':
    init_db()
    seed_data()
    app.run(debug=False)
