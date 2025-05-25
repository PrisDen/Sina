# Sina - The Disciplined Mentor

A local web application designed to help you build unshakeable discipline through task management, focus sessions, journaling, and personalized mentorship from Sina - your AI discipline coach.

## 🧠 About Sina

Sina is not your friend - she's your mentor. She adapts her tone based on your performance:
- **Encouraging** when you're doing well and building momentum
- **Strict** when you're falling behind and need accountability  
- **Motivational** when you need that extra push to keep going

## ✨ Features

### Phase 1 (Current Implementation)
- **User Authentication** - Secure local login with password encryption
- **Dashboard** - Personalized overview with Sina's daily message
- **Task Management** - Create, prioritize, and complete tasks with categories
- **Focus Sessions** - Built-in Pomodoro timer (25/5 minute cycles)
- **Daily Journal** - Reflection and mood tracking
- **Progress Tracking** - Streak counters and completion statistics
- **Sina's Personality** - Dynamic messaging based on your performance

### Phase 2 (Future Features)
- Habit tracking and streak calendars
- Advanced analytics and progress reports
- Gamification with achievements and badges
- Voice mode with text-to-speech
- Data export and backup options
- Dark mode and customization settings

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- A modern web browser

### Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/sina-project
   ```

2. **Set up virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://127.0.0.1:5000`

### First Time Setup

1. Click "Start your discipline journey" to create an account
2. Choose a username and secure password (minimum 6 characters)
3. Complete registration and you'll be taken to your dashboard
4. Meet Sina and start building your discipline!

## 📱 How to Use

### Dashboard
- View Sina's personalized message based on your recent performance
- Check your daily stats: tasks completed, focus time, current streak
- Use the quick timer for immediate focus sessions
- See your priority tasks and upcoming deadlines

### Task Management
- Click "Add Task" to create new tasks
- Set priority levels (High, Medium, Low) and categories
- Check off completed tasks to build your streak
- Tasks are automatically sorted by priority and deadline

### Focus Sessions
- Use the built-in Pomodoro timer (25 minutes work, 5 minutes break)
- Start, pause, or reset as needed
- Sessions are automatically logged to track your focus time
- Sina celebrates completed sessions with encouraging messages

### Daily Journal
- Reflect on your day in the journal section
- Write about your goals, challenges, and feelings
- Sina appreciates thoughtful reflection (minimum 10 characters)
- Journal entries are saved automatically

## 🎯 Sina's Personality System

Sina's tone adapts based on your weekly performance:

- **10+ tasks completed + 15+ focus sessions** → Encouraging tone
- **5+ tasks completed + 8+ focus sessions** → Motivational tone  
- **Less than 3 tasks or 5 sessions** → Strict tone

Her messages include:
- Performance-based feedback
- Motivational quotes
- Accountability reminders
- Celebration of achievements

## 🔒 Privacy & Security

- **100% Local** - All data stored locally in SQLite database
- **No External Requests** - No data sent to external servers
- **Secure Authentication** - Passwords hashed with bcrypt
- **Optional Encryption** - Future feature for journal/task encryption
- **No Tracking** - Sina is loyal only to you

## 🛠 Technical Details

### Tech Stack
- **Backend**: Python Flask
- **Database**: SQLite (local)
- **Frontend**: HTML5, CSS3 (Tailwind), Vanilla JavaScript
- **Security**: bcrypt password hashing
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)

### File Structure
```
sina/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── instance/
│   └── sina.db           # SQLite database
├── templates/
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── dashboard.html    # Main dashboard
└── static/
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── app.js        # JavaScript functionality
```

### Database Schema
- **users** - User accounts and settings
- **tasks** - Task management with priorities and categories
- **focus_sessions** - Pomodoro session tracking
- **journal_entries** - Daily reflection entries
- **habits** - Habit tracking (future feature)
- **user_settings** - Personalization options

## 🎨 Customization

### Sina's Quotes
Edit the `SINA_QUOTES` dictionary in `app.py` to customize Sina's motivational messages.

### Timer Duration
The default Pomodoro timer is 25 minutes. You can modify this in the JavaScript or add user settings.

### Color Scheme
The app uses a purple gradient theme. Modify the CSS variables in `style.css` to change colors.

## 🐛 Troubleshooting

### Common Issues

1. **Database errors**: Delete `instance/sina.db` and restart the app to recreate the database
2. **Port conflicts**: Change the port in `app.py` from 5000 to another number
3. **Permission errors**: Ensure the `instance/` directory is writable
4. **JavaScript errors**: Check browser console and ensure all files are loaded

### Development Mode
The app runs in debug mode by default. For production use:
```python
app.run(debug=False, host='127.0.0.1', port=5000)
```

## 🤝 Contributing

This is a personal productivity tool, but feel free to:
- Report bugs or issues
- Suggest new features for Sina's personality
- Improve the UI/UX design
- Add new motivational quotes

## 📄 License

This project is for personal use. Feel free to modify and adapt for your own discipline journey.

## 🎯 Philosophy

> "Discipline is the bridge between goals and accomplishment." - Sina

Sina believes that:
- Consistency beats perfection
- Small daily actions compound into major results
- Accountability accelerates growth
- Discipline is a skill that can be developed
- Your future self is counting on today's choices

---

**Start your discipline journey today. Sina is waiting to guide you to unshakeable discipline and long-term freedom.** 