# Sina - GitHub Pages Deployment

🧠 **Sina - Your Disciplined Mentor** is now available as a static web application on GitHub Pages!

## 🌐 Live Demo

**Access Sina here: [https://prisden.github.io/Sina/](https://prisden.github.io/Sina/)**

## ✨ What's New in the Static Version

This GitHub Pages deployment converts the original Flask application into a fully functional static website using:

- **localStorage** for data persistence (replaces SQLite database)
- **Client-side JavaScript** for all functionality (replaces Flask backend)
- **No server required** - runs entirely in your browser
- **Instant deployment** via GitHub Actions

## 🚀 Quick Start

1. **Visit the live site**: [https://prisden.github.io/Sina/](https://prisden.github.io/Sina/)
2. **Try the demo**: Click "Login as Demo User" to explore with pre-loaded data
3. **Create your account**: Register with any username/email (stored locally)
4. **Start building discipline**: Add tasks, run focus sessions, write journal entries

## 🔧 Features Available

### ✅ Fully Functional
- **User Authentication** (localStorage-based)
- **Task Management** (create, edit, delete, complete)
- **Pomodoro Timer** (25-minute focus sessions)
- **Journal System** (with mood tracking)
- **Dashboard Analytics** (progress tracking)
- **Sina's Adaptive Personality** (encouraging/motivational/strict modes)

### 🎯 Core Functionality
- **Task Prioritization** (high/medium/low)
- **Category Organization** (work/personal/study/health)
- **Deadline Management** (with overdue indicators)
- **Focus Session Tracking** (with notes)
- **Progress Statistics** (completion rates, streaks)
- **Recent Activity Feed** (timeline of accomplishments)

## 💾 Data Storage

**Important**: All data is stored in your browser's localStorage:
- ✅ **Private**: Data never leaves your device
- ✅ **Secure**: No external servers or databases
- ⚠️ **Local only**: Data is tied to your browser/device
- ⚠️ **Backup**: Clear browser data = lose your progress

### Data Persistence
- Tasks, journal entries, and focus sessions are saved automatically
- Data persists between browser sessions
- Multiple users can be created on the same device
- Demo account comes with sample data

## 🎨 User Interface

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Built with Tailwind CSS
- **Smooth Animations**: Fade-in effects and transitions
- **Intuitive Navigation**: Clear menu structure
- **Visual Feedback**: Progress bars, notifications, status indicators

## 🧠 Sina's Personality System

Sina adapts her mentorship style based on your performance:

- **🌟 Encouraging Mode** (80%+ completion): Celebrates your success
- **💪 Motivational Mode** (60-80% completion): Provides gentle guidance  
- **🎯 Strict Mode** (<60% completion): Holds you accountable

## 📱 Pages Overview

### 🏠 Landing Page (`index.html`)
- Beautiful hero section with Sina introduction
- Feature highlights and philosophy
- Call-to-action buttons

### 🔐 Authentication (`login.html`, `register.html`)
- Simple username/password system
- Demo account option
- Form validation and error handling

### 📊 Dashboard (`dashboard.html`)
- Today's progress overview
- Quick task management
- Journal quick-entry
- Recent activity feed
- Sina's adaptive messaging

### ✅ Tasks (`tasks.html`)
- Full task CRUD operations
- Advanced filtering and search
- Priority and category management
- Deadline tracking

### ⏰ Focus (`focus.html`)
- Pomodoro timer (25-minute sessions)
- Task selection for focused work
- Session notes and tracking
- Recent session history

### 📖 Journal (`journal.html`)
- Daily reflection entries
- Mood tracking (1-5 scale with emojis)
- Entry history and search
- Mood analytics

### 📈 Analytics (`analytics.html`)
- Progress visualization
- Completion statistics
- Productivity insights
- Goal tracking

## 🛠 Technical Implementation

### Frontend Stack
- **HTML5**: Semantic markup
- **Tailwind CSS**: Utility-first styling
- **Vanilla JavaScript**: No frameworks, pure JS
- **Font Awesome**: Icon library
- **Google Fonts**: Typography (Inter)

### Architecture
- **Object-Oriented JS**: Clean class-based structure
- **Event-Driven**: Responsive user interactions
- **Modular Design**: Separated concerns
- **localStorage API**: Client-side data persistence

### Key Classes
- `SinaApp`: Main application controller
- `PomodoroTimer`: Focus session management
- `NotificationSystem`: User feedback system

## 🚀 Deployment Process

This site is automatically deployed using GitHub Actions:

1. **Trigger**: Push to main/master branch
2. **Build**: Copy static files to `_site` directory
3. **Deploy**: Upload to GitHub Pages
4. **Live**: Available at the GitHub Pages URL

### Manual Deployment
If you fork this repository:
1. Enable GitHub Pages in repository settings
2. Set source to "GitHub Actions"
3. Push changes to trigger deployment

## 🔄 Migration from Flask Version

The static version maintains feature parity with the original Flask application:

| Flask Feature | Static Equivalent |
|---------------|-------------------|
| SQLite Database | localStorage |
| Flask Routes | Client-side routing |
| Jinja2 Templates | Static HTML |
| Python Backend | JavaScript Frontend |
| Session Management | localStorage auth |
| Server-side Validation | Client-side validation |

## 🎯 Philosophy

> "Discipline is the bridge between goals and accomplishment."

Sina embodies this philosophy through:
- **Consistent Structure**: Regular routines build habits
- **Adaptive Guidance**: Personalized feedback based on progress
- **Holistic Approach**: Tasks, focus, reflection, and analytics
- **Long-term Vision**: Building unshakeable discipline over time

## 🤝 Contributing

Want to improve Sina? Here's how:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your improvements
4. **Test** thoroughly
5. **Submit** a pull request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/Sina.git
cd Sina

# Open in browser (no build process needed!)
open index.html
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Pomodoro Technique**: Francesco Cirillo
- **Tailwind CSS**: Adam Wathan and team
- **Font Awesome**: Dave Gandy and team
- **GitHub Pages**: Free hosting for open source projects

---

**Start your discipline journey today**: [https://prisden.github.io/Sina/](https://prisden.github.io/Sina/)

*Built with ❤️ for those who choose discipline over regret.* 