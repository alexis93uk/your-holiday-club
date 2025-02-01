import os
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

# Create and configure the Flask application
app = Flask(__name__)

# Load SECRET_KEY from environment variable or use a fallback
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'some_secret_key')

# Path to the SQLite database
DATABASE = 'holiday_club.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            story_text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def seed_data():
    conn = get_db_connection()
    
    sample_stories = [
        ("Paris, France", "I visited the Eiffel Tower and enjoyed croissants by the Seine."),
        ("Tokyo, Japan", "I tried sushi at Tsukiji market and explored Shibuya Crossing."),
        ("Cairo, Egypt", "Saw the pyramids at Giza and experienced the local markets."),
        ("New York, USA", "Loved the hustle of Times Square and a stroll in Central Park."),
        ("Sydney, Australia", "Visited the Opera House and enjoyed Bondi Beach.")
    ]
    
    
    existing = conn.execute('SELECT COUNT(*) as count FROM stories').fetchone()
    if existing['count'] == 0:
        for location, story_text in sample_stories:
            conn.execute('INSERT INTO stories (location, story_text) VALUES (?, ?)',
                         (location, story_text))
        conn.commit()
    conn.close()


# ROUTES


@app.route('/')
def index():
    """
    Home page route.
    """
    return render_template('index.html')

@app.route('/about')
def about():
    """
    About page route.
    """
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Contact page route. For now, we just collect form data and flash a message.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
       
        flash("Thank you for your message. We'll get back to you soon!", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/viewstory')
def view_story():
    """
    View multiple stories route (lists them).
    """
    conn = get_db_connection()
    stories = conn.execute('SELECT * FROM stories').fetchall()
    conn.close()
    return render_template('viewstory.html', stories=stories)

@app.route('/story/<int:story_id>')
def story_detail(story_id):
    """
    Display a single story with potential images, etc.
    """
    conn = get_db_connection()
    story = conn.execute('SELECT * FROM stories WHERE id = ?', (story_id,)).fetchone()
    conn.close()
    
    if story is None:
        flash("Story not found!", "error")
        return redirect(url_for('view_story'))
    
    return render_template('story.html', story=story)

@app.route('/addstory', methods=['GET', 'POST'])
def add_story():
    """
    Adding a new story. Requires a location and a story description.
    """
    if request.method == 'POST':
        location = request.form.get('location')
        story_text = request.form.get('story_text')
        
        if not location or not story_text:
            flash("Please provide both location and story text.", "error")
            return redirect(url_for('add_story'))
        
        conn = get_db_connection()
        conn.execute('INSERT INTO stories (location, story_text) VALUES (?, ?)',
                     (location, story_text))
        conn.commit()
        conn.close()
        
        flash("Story added successfully!", "success")
        return redirect(url_for('view_story'))
    return render_template('addstory.html')

@app.route('/editstory/<int:story_id>', methods=['GET', 'POST'])
def edit_story(story_id):
    """
    Edit an existing story.
    """
    conn = get_db_connection()
    story = conn.execute('SELECT * FROM stories WHERE id = ?', (story_id,)).fetchone()
    
    if story is None:
        conn.close()
        flash("Story not found!", "error")
        return redirect(url_for('view_story'))
    
    if request.method == 'POST':
        location = request.form.get('location')
        story_text = request.form.get('story_text')
        
        if not location or not story_text:
            flash("Please fill out all fields.", "error")
            return redirect(url_for('edit_story', story_id=story_id))
        
        conn.execute('UPDATE stories SET location = ?, story_text = ? WHERE id = ?',
                     (location, story_text, story_id))
        conn.commit()
        conn.close()
        
        flash("Story updated successfully!", "success")
        return redirect(url_for('view_story'))
    
    conn.close()
    return render_template('editstory.html', story=story)

@app.route('/deletestory/<int:story_id>', methods=['GET', 'POST'])
def delete_story(story_id):
    """
    Delete a story from the database.
    """
    conn = get_db_connection()
    story = conn.execute('SELECT * FROM stories WHERE id = ?', (story_id,)).fetchone()
    
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


# MAIN EXECUTION

if __name__ == '__main__':
    init_db()
    seed_data()
    
    # Run the Flask app
    # For production, set debug=False; for development, debug=True
    app.run(debug=False)
