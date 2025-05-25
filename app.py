from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlite3
import os
from functools import wraps
import json
import random
import logging

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'sina_mentor_secret_key_change_in_production')

# Configure static files
app.static_folder = 'static'
app.static_url_path = '/static'

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Add error handlers
@app.errorhandler(403)
def forbidden(error):
    app.logger.error(f"403 Forbidden: {request.url}")
    return "Access Forbidden", 403

@app.errorhandler(404)
def not_found(error):
    app.logger.error(f"404 Not Found: {request.url}")
    return "Page Not Found", 404

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
    """Generate Sina's personalized message based on user performance and deadlines"""
    conn = sqlite3.connect('instance/sina.db')
    cursor = conn.cursor()
    
    # Check for overdue and approaching deadlines first
    now = datetime.now()
    today = now.date()
    
    # Check overdue tasks
    cursor.execute('''
        SELECT title, deadline FROM tasks 
        WHERE user_id = ? AND completed = FALSE AND deadline IS NOT NULL 
        AND datetime(deadline) < datetime('now')
        ORDER BY deadline ASC
        LIMIT 3
    ''', (user_id,))
    overdue_tasks = cursor.fetchall()
    
    # Check tasks due within 24 hours
    tomorrow = now + timedelta(hours=24)
    cursor.execute('''
        SELECT title, deadline FROM tasks 
        WHERE user_id = ? AND completed = FALSE AND deadline IS NOT NULL 
        AND datetime(deadline) BETWEEN datetime('now') AND datetime(?)
        ORDER BY deadline ASC
        LIMIT 3
    ''', (user_id, tomorrow.isoformat()))
    urgent_tasks = cursor.fetchall()
    
    # If there are overdue tasks, Sina gets VERY strict
    if overdue_tasks:
        task_titles = [task[0] for task in overdue_tasks[:2]]
        if len(overdue_tasks) == 1:
            message = f"UNACCEPTABLE! '{task_titles[0]}' is OVERDUE. Stop making excuses and GET IT DONE NOW!"
        else:
            message = f"This is embarrassing. You have {len(overdue_tasks)} overdue tasks including '{task_titles[0]}' and '{task_titles[1]}'. Your discipline is failing you."
        
        strict_quotes = [
            "Deadlines are not suggestions. They are commitments to your future self.",
            "Every missed deadline is a broken promise to yourself.",
            "Procrastination is the assassination of motivation.",
            "You can't negotiate with time. It doesn't care about your excuses."
        ]
        quote = random.choice(strict_quotes)
        return {'message': message, 'quote': quote, 'tone': 'strict'}
    
    # If there are urgent tasks (due within 24 hours), Sina gets strict
    if urgent_tasks:
        task_title = urgent_tasks[0][0]
        deadline_str = urgent_tasks[0][1]
        try:
            if 'T' in deadline_str:
                deadline = datetime.fromisoformat(deadline_str.replace('T', ' '))
            else:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
            
            hours_left = (deadline - now).total_seconds() / 3600
            
            if hours_left < 2:
                message = f"URGENT! '{task_title}' is due in {int(hours_left)} hours. Drop everything and focus NOW!"
            elif hours_left < 6:
                message = f"Time is running out! '{task_title}' is due in {int(hours_left)} hours. No more delays!"
            else:
                message = f"'{task_title}' is due within 24 hours. Time to get serious and prioritize this task."
        except:
            message = f"'{task_title}' has an approaching deadline. Don't let it become overdue!"
        
        urgent_quotes = [
            "Urgency is the mother of efficiency.",
            "When time is short, excuses are shorter.",
            "The clock is ticking. Your discipline is being tested.",
            "Pressure makes diamonds. What will it make of you?"
        ]
        quote = random.choice(urgent_quotes)
        return {'message': message, 'quote': quote, 'tone': 'strict'}
    
    # Regular performance-based messaging
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

@app.route('/test')
def test():
    """Simple test route to verify app is working"""
    return jsonify({
        'status': 'success',
        'message': 'Sina app is running correctly!',
        'timestamp': datetime.now().isoformat()
    })

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
    
    # Today's tasks - Show all pending tasks + tasks completed today
    cursor.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE user_id = ? AND completed = FALSE
    ''', (user_id,))
    pending_tasks_count = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE user_id = ? AND completed = TRUE AND DATE(completed_at) = ?
    ''', (user_id, today))
    completed_today = cursor.fetchone()[0]
    
    # Total tasks for today = pending tasks + completed today
    today_tasks = pending_tasks_count + completed_today
    
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
        SELECT id, title, priority, category, deadline, in_progress FROM tasks 
        WHERE user_id = ? AND completed = FALSE 
        ORDER BY 
            in_progress DESC,
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

@app.route('/tasks')
@login_required
def tasks():
    user_id = session['user_id']
    conn = sqlite3.connect('instance/sina.db')
    cursor = conn.cursor()
    
    # Get all tasks for the user
    cursor.execute('''
        SELECT id, title, description, priority, category, deadline, completed, created_at, completed_at
        FROM tasks 
        WHERE user_id = ? 
        ORDER BY 
            completed ASC,
            CASE priority 
                WHEN 'high' THEN 1 
                WHEN 'medium' THEN 2 
                WHEN 'low' THEN 3 
            END,
            deadline ASC,
            created_at DESC
    ''', (user_id,))
    
    tasks_data = cursor.fetchall()
    
    # Convert to objects for easier template access
    tasks = []
    for task_data in tasks_data:
        # Handle different datetime formats
        def parse_datetime(date_str):
            if not date_str:
                return None
            try:
                # Try ISO format first (from HTML datetime-local input)
                if 'T' in date_str:
                    return datetime.fromisoformat(date_str.replace('T', ' '))
                # Try standard SQLite format
                return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    # Try date only format
                    return datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    return None
        
        task = {
            'id': task_data[0],
            'title': task_data[1],
            'description': task_data[2],
            'priority': task_data[3],
            'category': task_data[4],
            'deadline': parse_datetime(task_data[5]),
            'completed': task_data[6],
            'created_at': parse_datetime(task_data[7]),
            'completed_at': parse_datetime(task_data[8])
        }
        tasks.append(task)
    
    # Calculate statistics
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t['completed']])
    pending_tasks = len([t for t in tasks if not t['completed']])
    
    now = datetime.now()
    overdue_tasks = len([t for t in tasks if not t['completed'] and t['deadline'] and t['deadline'] < now])
    
    conn.close()
    
    return render_template('tasks.html',
                         tasks=tasks,
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         pending_tasks=pending_tasks,
                         overdue_tasks=overdue_tasks,
                         now=now)

@app.route('/focus')
@login_required
def focus():
    user_id = session['user_id']
    conn = sqlite3.connect('instance/sina.db')
    cursor = conn.cursor()
    
    # Get today's session stats
    today = datetime.now().date()
    cursor.execute('''
        SELECT COUNT(*), COALESCE(SUM(duration), 0) FROM focus_sessions 
        WHERE user_id = ? AND DATE(session_date) = ?
    ''', (user_id, today))
    focus_stats = cursor.fetchone()
    today_sessions = focus_stats[0]
    today_minutes = focus_stats[1]
    
    # Get recent sessions
    cursor.execute('''
        SELECT fs.duration, fs.notes, fs.session_date, t.title as task_title
        FROM focus_sessions fs
        LEFT JOIN tasks t ON fs.task_id = t.id
        WHERE fs.user_id = ?
        ORDER BY fs.session_date DESC
        LIMIT 10
    ''', (user_id,))
    
    sessions_data = cursor.fetchall()
    sessions = []
    for focus_session_data in sessions_data:
        # Handle datetime parsing safely
        try:
            session_date = datetime.strptime(focus_session_data[2], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                session_date = datetime.fromisoformat(focus_session_data[2].replace('T', ' '))
            except ValueError:
                session_date = datetime.now()  # Fallback
        
        focus_session = {
            'duration': focus_session_data[0],
            'notes': focus_session_data[1],
            'session_date': session_date,
            'task_title': focus_session_data[3]
        }
        sessions.append(focus_session)
    
    conn.close()
    
    return render_template('focus.html',
                         today_sessions=today_sessions,
                         today_minutes=today_minutes,
                         sessions=sessions)

@app.route('/journal')
@login_required
def journal():
    user_id = session['user_id']
    conn = sqlite3.connect('instance/sina.db')
    cursor = conn.cursor()
    
    today = datetime.now().date()
    
    # Get today's entry
    cursor.execute('''
        SELECT content, mood, created_at FROM journal_entries 
        WHERE user_id = ? AND entry_date = ?
    ''', (user_id, today))
    today_entry_data = cursor.fetchone()
    
    today_entry = None
    if today_entry_data:
        # Handle datetime parsing safely
        try:
            created_at = datetime.strptime(today_entry_data[2], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                created_at = datetime.fromisoformat(today_entry_data[2].replace('T', ' '))
            except ValueError:
                created_at = datetime.now()
        
        today_entry = {
            'content': today_entry_data[0],
            'mood': today_entry_data[1],
            'created_at': created_at
        }
    
    # Get recent entries
    cursor.execute('''
        SELECT content, mood, entry_date, created_at FROM journal_entries 
        WHERE user_id = ? 
        ORDER BY entry_date DESC 
        LIMIT 10
    ''', (user_id,))
    
    entries_data = cursor.fetchall()
    entries = []
    for entry_data in entries_data:
        # Handle datetime parsing safely
        try:
            entry_date = datetime.strptime(entry_data[2], '%Y-%m-%d').date()
        except ValueError:
            entry_date = datetime.now().date()
        
        try:
            created_at = datetime.strptime(entry_data[3], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                created_at = datetime.fromisoformat(entry_data[3].replace('T', ' '))
            except ValueError:
                created_at = datetime.now()
        
        entry = {
            'content': entry_data[0],
            'mood': entry_data[1],
            'entry_date': entry_date,
            'created_at': created_at
        }
        entries.append(entry)
    
    # Calculate stats
    cursor.execute('SELECT COUNT(*) FROM journal_entries WHERE user_id = ?', (user_id,))
    total_entries = cursor.fetchone()[0]
    
    cursor.execute('SELECT AVG(mood) FROM journal_entries WHERE user_id = ?', (user_id,))
    avg_mood_result = cursor.fetchone()[0]
    average_mood = round(avg_mood_result, 1) if avg_mood_result else 3.0
    
    # Calculate journal streak
    cursor.execute('''
        SELECT entry_date FROM journal_entries 
        WHERE user_id = ? 
        ORDER BY entry_date DESC
    ''', (user_id,))
    entry_dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in cursor.fetchall()]
    
    journal_streak = 0
    if entry_dates:
        current_date = datetime.now().date()
        for date in entry_dates:
            if date == current_date or date == current_date - timedelta(days=journal_streak):
                if date == current_date - timedelta(days=journal_streak):
                    journal_streak += 1
                current_date = date
            else:
                break
    
    conn.close()
    
    return render_template('journal.html',
                         today_entry=today_entry,
                         entries=entries,
                         total_entries=total_entries,
                         average_mood=average_mood,
                         journal_streak=journal_streak,
                         today_date=today.strftime('%B %d, %Y'))

@app.route('/analytics')
@login_required
def analytics():
    user_id = session['user_id']
    conn = sqlite3.connect('instance/sina.db')
    cursor = conn.cursor()
    
    # Basic stats
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE user_id = ?', (user_id,))
    total_tasks = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = TRUE', (user_id,))
    completed_tasks = cursor.fetchone()[0]
    
    completion_rate = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
    
    cursor.execute('SELECT COALESCE(SUM(duration), 0) FROM focus_sessions WHERE user_id = ?', (user_id,))
    total_focus_minutes = cursor.fetchone()[0]
    total_focus_hours = round(total_focus_minutes / 60, 1)
    
    cursor.execute('SELECT COUNT(*) FROM journal_entries WHERE user_id = ?', (user_id,))
    total_entries = cursor.fetchone()[0]
    
    # Mock data for demo
    stats = {
        'total_tasks': total_tasks,
        'completion_rate': completion_rate,
        'total_focus_hours': total_focus_hours,
        'avg_daily_focus': round(total_focus_hours / 30, 1),  # Assuming 30 days
        'total_entries': total_entries,
        'journal_streak': 5,  # Mock data
        'best_streak': 12,    # Mock data
        'avg_session_length': 25,
        'total_sessions': cursor.execute('SELECT COUNT(*) FROM focus_sessions WHERE user_id = ?', (user_id,)).fetchone()[0],
        'best_focus_day': 'Monday'
    }
    
    # Real weekly data based on actual task completions
    weekly_data = []
    today = datetime.now().date()
    for i in range(7):
        day_date = today - timedelta(days=6-i)
        day_name = day_date.strftime('%A')
        
        cursor.execute('''
            SELECT COUNT(*) FROM tasks 
            WHERE user_id = ? AND completed = TRUE AND DATE(completed_at) = ?
        ''', (user_id, day_date))
        completed = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM tasks 
            WHERE user_id = ? AND (DATE(created_at) <= ? AND (completed = FALSE OR DATE(completed_at) >= ?))
        ''', (user_id, day_date, day_date))
        total = cursor.fetchone()[0]
        
        completion_percentage = round((completed / total * 100) if total > 0 else 0)
        
        weekly_data.append({
            'name': day_name,
            'completed': completed,
            'total': total,
            'completion_percentage': completion_percentage
        })
    
    # Real mood trends based on journal entries
    cursor.execute('''
        SELECT mood, COUNT(*) FROM journal_entries 
        WHERE user_id = ? 
        GROUP BY mood
    ''', (user_id,))
    mood_data = cursor.fetchall()
    
    mood_mapping = {
        1: {'emoji': '😢', 'label': 'Terrible'},
        2: {'emoji': '😕', 'label': 'Poor'},
        3: {'emoji': '😐', 'label': 'Neutral'},
        4: {'emoji': '😊', 'label': 'Good'},
        5: {'emoji': '😄', 'label': 'Excellent'}
    }
    
    total_mood_entries = sum([count for _, count in mood_data])
    mood_trends = []
    
    for mood_value in range(1, 6):
        count = next((count for mood, count in mood_data if mood == mood_value), 0)
        percentage = round((count / total_mood_entries * 100) if total_mood_entries > 0 else 0)
        
        mood_trends.append({
            'emoji': mood_mapping[mood_value]['emoji'],
            'label': mood_mapping[mood_value]['label'],
            'count': count,
            'percentage': percentage
        })
    
    # Task categories
    cursor.execute('''
        SELECT category, COUNT(*) FROM tasks WHERE user_id = ? GROUP BY category
    ''', (user_id,))
    category_data = cursor.fetchall()
    
    task_categories = []
    for cat_data in category_data:
        task_categories.append({
            'name': cat_data[0],
            'count': cat_data[1],
            'percentage': round((cat_data[1] / total_tasks * 100) if total_tasks > 0 else 0, 1)
        })
    
    # Achievements (mock)
    achievements = [
        {'icon': '🎯', 'title': 'First Task', 'description': 'Completed your first task'},
        {'icon': '🔥', 'title': 'Week Warrior', 'description': '7 days of consistent progress'},
        {'icon': '⏰', 'title': 'Focus Master', 'description': '10 focus sessions completed'},
        {'icon': '📝', 'title': 'Reflective Soul', 'description': '5 journal entries written'}
    ]
    
    conn.close()
    
    return render_template('analytics.html',
                         stats=stats,
                         weekly_data=weekly_data,
                         mood_trends=mood_trends,
                         task_categories=task_categories,
                         achievements=achievements)

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
    mood = data.get('mood', 5)  # Default mood is 5 (happy)
    
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
                UPDATE journal_entries SET content = ?, mood = ?, created_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (content, mood, existing[0]))
        else:
            # Create new entry
            cursor.execute('''
                INSERT INTO journal_entries (user_id, content, mood, entry_date)
                VALUES (?, ?, ?, ?)
            ''', (user_id, content, mood, today))
        
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
    
    # Get stats - Use same logic as dashboard route
    cursor.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE user_id = ? AND completed = FALSE
    ''', (user_id,))
    pending_tasks_count = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE user_id = ? AND completed = TRUE AND DATE(completed_at) = ?
    ''', (user_id, today))
    completed_today = cursor.fetchone()[0]
    
    # Total tasks for today = pending tasks + completed today
    today_tasks = pending_tasks_count + completed_today
    
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

@app.route('/api/deadline/check')
@login_required
def api_check_deadlines():
    user_id = session['user_id']
    conn = sqlite3.connect('instance/sina.db')
    cursor = conn.cursor()
    
    now = datetime.now()
    
    # Check overdue tasks
    cursor.execute('''
        SELECT title, deadline FROM tasks 
        WHERE user_id = ? AND completed = FALSE AND deadline IS NOT NULL 
        AND datetime(deadline) < datetime('now')
        ORDER BY deadline ASC
    ''', (user_id,))
    overdue_data = cursor.fetchall()
    
    overdue_tasks = []
    for task_title, deadline_str in overdue_data:
        try:
            if 'T' in deadline_str:
                deadline = datetime.fromisoformat(deadline_str.replace('T', ' '))
            else:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
            
            overdue_hours = (now - deadline).total_seconds() / 3600
            
            if overdue_hours < 24:
                overdue_text = f"{int(overdue_hours)} hours ago"
            else:
                overdue_days = int(overdue_hours / 24)
                overdue_text = f"{overdue_days} day{'s' if overdue_days > 1 else ''} ago"
            
            overdue_tasks.append({
                'title': task_title,
                'overdue_text': overdue_text
            })
        except:
            overdue_tasks.append({
                'title': task_title,
                'overdue_text': 'some time ago'
            })
    
    # Check urgent tasks (due within 6 hours)
    urgent_deadline = now + timedelta(hours=6)
    cursor.execute('''
        SELECT title, deadline FROM tasks 
        WHERE user_id = ? AND completed = FALSE AND deadline IS NOT NULL 
        AND datetime(deadline) BETWEEN datetime('now') AND datetime(?)
        ORDER BY deadline ASC
    ''', (user_id, urgent_deadline.isoformat()))
    urgent_data = cursor.fetchall()
    
    urgent_tasks = []
    for task_title, deadline_str in urgent_data:
        try:
            if 'T' in deadline_str:
                deadline = datetime.fromisoformat(deadline_str.replace('T', ' '))
            else:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
            
            hours_left = (deadline - now).total_seconds() / 3600
            
            if hours_left < 1:
                time_left = f"{int(hours_left * 60)} minutes"
            else:
                time_left = f"{int(hours_left)} hours"
            
            urgent_tasks.append({
                'title': task_title,
                'time_left': time_left
            })
        except:
            urgent_tasks.append({
                'title': task_title,
                'time_left': 'soon'
            })
    
    conn.close()
    
    return jsonify({
        'overdue': overdue_tasks,
        'urgent': urgent_tasks
    })

@app.route('/api/tasks/in-progress', methods=['POST'])
@login_required
def api_mark_task_in_progress():
    data = request.get_json()
    task_id = data['task_id']
    user_id = session['user_id']
    
    try:
        conn = sqlite3.connect('instance/sina.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tasks SET in_progress = TRUE
            WHERE id = ? AND user_id = ?
        ''', (task_id, user_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Task marked as in progress'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@login_required
def api_get_task(task_id):
    user_id = session['user_id']
    
    try:
        conn = sqlite3.connect('instance/sina.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, description, priority, category, deadline, completed, in_progress
            FROM tasks 
            WHERE id = ? AND user_id = ?
        ''', (task_id, user_id))
        
        task_data = cursor.fetchone()
        conn.close()
        
        if task_data:
            # Handle datetime formatting for frontend
            deadline = task_data[5]
            if deadline:
                try:
                    if 'T' in deadline:
                        # Already in ISO format
                        formatted_deadline = deadline
                    else:
                        # Convert SQLite format to ISO format for datetime-local input
                        dt = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
                        formatted_deadline = dt.strftime('%Y-%m-%dT%H:%M')
                except:
                    formatted_deadline = deadline
            else:
                formatted_deadline = ''
            
            task = {
                'id': task_data[0],
                'title': task_data[1],
                'description': task_data[2],
                'priority': task_data[3],
                'category': task_data[4],
                'deadline': formatted_deadline,
                'completed': task_data[6],
                'in_progress': task_data[7]
            }
            return jsonify(task)
        else:
            return jsonify({'error': 'Task not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def api_update_task(task_id):
    data = request.get_json()
    user_id = session['user_id']
    
    try:
        conn = sqlite3.connect('instance/sina.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tasks SET 
                title = ?, 
                description = ?, 
                priority = ?, 
                category = ?, 
                deadline = ?
            WHERE id = ? AND user_id = ?
        ''', (data['title'], data.get('description', ''), 
              data.get('priority', 'medium'), data.get('category', 'personal'),
              data.get('deadline') if data.get('deadline') else None,
              task_id, user_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Task updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sessions/start', methods=['POST'])
@login_required
def api_start_focus_session():
    data = request.get_json()
    user_id = session['user_id']
    
    try:
        conn = sqlite3.connect('instance/sina.db')
        cursor = conn.cursor()
        
        # Log the session start (we'll update with actual duration when completed)
        cursor.execute('''
            INSERT INTO focus_sessions (user_id, task_id, duration, notes)
            VALUES (?, ?, ?, ?)
        ''', (user_id, data.get('task_id'), 0, data.get('notes', '')))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'session_id': session_id, 'message': 'Focus session started'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    init_db()
    
    # Production configuration
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port, threaded=True) 