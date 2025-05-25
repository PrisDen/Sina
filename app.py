from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlite3
import os
from functools import wraps
import json
import random

app = Flask(__name__)
app.secret_key = 'sina_mentor_secret_key_change_in_production'

# Database initialization
def init_db():
    conn = sqlite3.connect('instance/sina.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            secure_mode BOOLEAN DEFAULT FALSE,
            pin TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'medium',
            category TEXT DEFAULT 'personal',
            deadline TIMESTAMP,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Focus sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS focus_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task_id INTEGER,
            duration INTEGER NOT NULL,
            notes TEXT,
            session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        )
    ''')
    
    # Journal entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            mood INTEGER DEFAULT 5,
            entry_date DATE DEFAULT CURRENT_DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Habits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            frequency TEXT DEFAULT 'daily',
            target_count INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Habit tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habit_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completion_date DATE DEFAULT CURRENT_DATE,
            completed BOOLEAN DEFAULT TRUE,
            notes TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        )
    ''')
    
    # User settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            persona_tone TEXT DEFAULT 'balanced',
            timer_work_duration INTEGER DEFAULT 25,
            timer_break_duration INTEGER DEFAULT 5,
            dark_mode BOOLEAN DEFAULT FALSE,
            notifications BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Sina's quotes and messages
SINA_QUOTES = {
    'motivational': [
        "Discipline is the bridge between goals and accomplishment.",
        "You don't have to be great to get started, but you have to get started to be great.",
        "The pain of discipline weighs ounces, but the pain of regret weighs tons.",
        "Success is the sum of small efforts repeated day in and day out."
    ],
    'strict': [
        "Excuses will always be there for you. Opportunities won't.",
        "You can't have a million dollar dream with a minimum wage work ethic.",
        "Stop waiting for motivation. Start building discipline.",
        "Your future self is counting on what you do today."
    ],
    'encouraging': [
        "Every small step forward is progress worth celebrating.",
        "You're stronger than you think and more capable than you know.",
        "Consistency beats perfection every single time.",
        "I believe in you, even when you don't believe in yourself."
    ]
}

def get_sina_message(user_id):
    """Generate Sina's personalized message based on user performance"""
    conn = sqlite3.connect('instance/sina.db')
    cursor = conn.cursor()
    
    # Get recent performance data
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    # Check completed tasks this week
    cursor.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE user_id = ? AND completed = TRUE 
        AND DATE(completed_at) >= ?
    ''', (user_id, week_ago))
    completed_tasks = cursor.fetchone()[0]
    
    # Check focus sessions this week
    cursor.execute('''
        SELECT COUNT(*), SUM(duration) FROM focus_sessions 
        WHERE user_id = ? AND DATE(session_date) >= ?
    ''', (user_id, week_ago))
    session_data = cursor.fetchone()
    session_count = session_data[0] or 0
    total_minutes = session_data[1] or 0
    
    conn.close()
    
    # Determine Sina's tone based on performance
    if completed_tasks >= 10 and session_count >= 15:
        tone = 'encouraging'
        message = f"Outstanding work! {completed_tasks} tasks completed and {total_minutes} minutes of focused work this week. You're building real momentum."
    elif completed_tasks >= 5 and session_count >= 8:
        tone = 'motivational'
        message = f"Good progress with {completed_tasks} tasks done. Let's push for even more focus sessions - you had {session_count} this week."
    elif completed_tasks < 3 or session_count < 5:
        tone = 'strict'
        message = f"We need to talk. Only {completed_tasks} tasks completed and {session_count} focus sessions this week. Your future self deserves better."
    else:
        tone = 'motivational'
        message = f"You're on track with {completed_tasks} tasks completed. Let's maintain this momentum and add more focused work sessions."
    
    quote = random.choice(SINA_QUOTES[tone])
    return {'message': message, 'quote': quote, 'tone': tone}

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('instance/sina.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            flash('Welcome back! Sina is ready to help you stay disciplined.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Sina expects better attention to detail.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match. Sina values consistency.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters. Security matters.', 'error')
            return render_template('register.html')
        
        password_hash = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect('instance/sina.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                         (username, password_hash))
            user_id = cursor.lastrowid
            
            # Create default settings for new user
            cursor.execute('''
                INSERT INTO user_settings (user_id) VALUES (?)
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            
            session['user_id'] = user_id
            session['username'] = username
            flash('Welcome to your discipline journey! Sina is here to guide you.', 'success')
            return redirect(url_for('dashboard'))
            
        except sqlite3.IntegrityError:
            flash('Username already exists. Choose another one.', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out. Remember, discipline is a daily choice.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    conn = sqlite3.connect('instance/sina.db')
    cursor = conn.cursor()
    
    # Get today's stats
    today = datetime.now().date()
    
    # Today's tasks
    cursor.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE user_id = ? AND DATE(created_at) = ?
    ''', (user_id, today))
    today_tasks = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE user_id = ? AND completed = TRUE AND DATE(completed_at) = ?
    ''', (user_id, today))
    completed_today = cursor.fetchone()[0]
    
    # Today's focus sessions
    cursor.execute('''
        SELECT COUNT(*), COALESCE(SUM(duration), 0) FROM focus_sessions 
        WHERE user_id = ? AND DATE(session_date) = ?
    ''', (user_id, today))
    session_data = cursor.fetchone()
    today_sessions = session_data[0]
    today_minutes = session_data[1]
    
    # Current streak (consecutive days with completed tasks)
    cursor.execute('''
        SELECT DATE(completed_at) FROM tasks 
        WHERE user_id = ? AND completed = TRUE 
        ORDER BY completed_at DESC
    ''', (user_id,))
    completion_dates = [row[0] for row in cursor.fetchall()]
    
    streak = 0
    if completion_dates:
        current_date = datetime.now().date()
        for date_str in completion_dates:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date_obj == current_date or date_obj == current_date - timedelta(days=streak):
                if date_obj == current_date - timedelta(days=streak):
                    streak += 1
                current_date = date_obj
            else:
                break
    
    # Get pending tasks
    cursor.execute('''
        SELECT id, title, priority, category, deadline FROM tasks 
        WHERE user_id = ? AND completed = FALSE 
        ORDER BY 
            CASE priority 
                WHEN 'high' THEN 1 
                WHEN 'medium' THEN 2 
                WHEN 'low' THEN 3 
            END,
            deadline ASC
        LIMIT 5
    ''', (user_id,))
    pending_tasks = cursor.fetchall()
    
    conn.close()
    
    # Get Sina's message
    sina_data = get_sina_message(user_id)
    
    return render_template('dashboard.html', 
                         today_tasks=today_tasks,
                         completed_today=completed_today,
                         today_sessions=today_sessions,
                         today_minutes=today_minutes,
                         streak=streak,
                         pending_tasks=pending_tasks,
                         sina_message=sina_data['message'],
                         sina_quote=sina_data['quote'],
                         sina_tone=sina_data['tone'])

# API Routes
@app.route('/api/tasks/create', methods=['POST'])
@login_required
def api_create_task():
    data = request.get_json()
    user_id = session['user_id']
    
    try:
        conn = sqlite3.connect('instance/sina.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tasks (user_id, title, description, priority, category, deadline)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, data['title'], data.get('description', ''), 
              data.get('priority', 'medium'), data.get('category', 'personal'),
              data.get('deadline') if data.get('deadline') else None))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Task created successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/tasks/complete', methods=['POST'])
@login_required
def api_complete_task():
    data = request.get_json()
    task_id = data['task_id']
    user_id = session['user_id']
    
    try:
        conn = sqlite3.connect('instance/sina.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tasks SET completed = TRUE, completed_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        ''', (task_id, user_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Task completed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/tasks/uncomplete', methods=['POST'])
@login_required
def api_uncomplete_task():
    data = request.get_json()
    task_id = data['task_id']
    user_id = session['user_id']
    
    try:
        conn = sqlite3.connect('instance/sina.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tasks SET completed = FALSE, completed_at = NULL
            WHERE id = ? AND user_id = ?
        ''', (task_id, user_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Task uncompleted'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sessions/log', methods=['POST'])
@login_required
def api_log_session():
    data = request.get_json()
    user_id = session['user_id']
    
    try:
        conn = sqlite3.connect('instance/sina.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO focus_sessions (user_id, duration, notes)
            VALUES (?, ?, ?)
        ''', (user_id, data['duration'], data.get('notes', '')))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Session logged'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/journal/save', methods=['POST'])
@login_required
def api_save_journal():
    data = request.get_json()
    user_id = session['user_id']
    content = data['content']
    
    try:
        conn = sqlite3.connect('instance/sina.db')
        cursor = conn.cursor()
        
        # Check if entry exists for today
        today = datetime.now().date()
        cursor.execute('''
            SELECT id FROM journal_entries 
            WHERE user_id = ? AND entry_date = ?
        ''', (user_id, today))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing entry
            cursor.execute('''
                UPDATE journal_entries SET content = ?, created_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (content, existing[0]))
        else:
            # Create new entry
            cursor.execute('''
                INSERT INTO journal_entries (user_id, content, entry_date)
                VALUES (?, ?, ?)
            ''', (user_id, content, today))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Journal entry saved'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/dashboard/stats')
@login_required
def api_dashboard_stats():
    user_id = session['user_id']
    conn = sqlite3.connect('instance/sina.db')
    cursor = conn.cursor()
    
    today = datetime.now().date()
    
    # Get stats
    cursor.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE user_id = ? AND DATE(created_at) = ?
    ''', (user_id, today))
    today_tasks = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE user_id = ? AND completed = TRUE AND DATE(completed_at) = ?
    ''', (user_id, today))
    completed_today = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COALESCE(SUM(duration), 0) FROM focus_sessions 
        WHERE user_id = ? AND DATE(session_date) = ?
    ''', (user_id, today))
    today_minutes = cursor.fetchone()[0]
    
    # Calculate streak
    cursor.execute('''
        SELECT DATE(completed_at) FROM tasks 
        WHERE user_id = ? AND completed = TRUE 
        ORDER BY completed_at DESC
    ''', (user_id,))
    completion_dates = [row[0] for row in cursor.fetchall()]
    
    streak = 0
    if completion_dates:
        current_date = datetime.now().date()
        for date_str in completion_dates:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date_obj == current_date or date_obj == current_date - timedelta(days=streak):
                if date_obj == current_date - timedelta(days=streak):
                    streak += 1
                current_date = date_obj
            else:
                break
    
    conn.close()
    
    return jsonify({
        'today_tasks': today_tasks,
        'completed_today': completed_today,
        'today_minutes': today_minutes,
        'streak': streak
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000) 