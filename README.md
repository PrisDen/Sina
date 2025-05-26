# Sina - Your Disciplined Mentor

**Build unshakeable discipline through intelligent task management, focused work sessions, and personalized mentorship.**

## Overview

Sina is a web-based productivity application designed to help users develop lasting discipline through structured task management, Pomodoro-style focus sessions, reflective journaling, and adaptive mentorship. The application runs entirely in your browser with no server dependencies.

## Live Application

**Access Sina at:** [Your Netlify URL will go here]

## Key Features

### Task Management
- Create, organize, and prioritize tasks with deadlines
- Categorize tasks by type (work, personal, study, health)
- Advanced filtering and search capabilities
- Progress tracking and completion analytics

### Focus Sessions
- Pomodoro timer with 25-minute focused work periods
- Task-specific focus sessions with note-taking
- Session history and productivity insights
- Automatic progress tracking

### Personal Journaling
- Daily reflection entries with mood tracking
- Historical journal browsing and search
- Mood analytics and patterns
- Private, secure local storage

### Adaptive Mentorship
- Sina's personality adapts based on your performance
- Encouraging mode for high achievers
- Motivational guidance for steady progress
- Accountability mode for those needing structure

### Analytics Dashboard
- Progress visualization and statistics
- Completion rates and productivity trends
- Goal tracking and milestone recognition
- Performance insights over time

## Data Privacy and Security

### Local Storage Architecture
- **All user data remains on your device** - stored in browser localStorage
- **No data transmission** to external servers or databases
- **Complete privacy** - your information never leaves your browser
- **No account required** - create local profiles without email or personal information

### Netlify Hosting
- Netlify hosts only the static application files (HTML, CSS, JavaScript)
- No user data is stored on Netlify servers
- No backend database or server-side processing
- Your tasks, journal entries, and settings remain private on your device

### Data Portability
- Data stored in standard JSON format
- Export capabilities through browser developer tools
- No vendor lock-in or proprietary formats
- Complete user control over personal information

## Technical Architecture

### Frontend Technologies
- **HTML5** - Semantic markup and structure
- **Tailwind CSS** - Modern, responsive styling
- **Vanilla JavaScript** - No framework dependencies
- **Font Awesome** - Professional iconography
- **Google Fonts** - Clean typography

### Application Structure
- Object-oriented JavaScript architecture
- Event-driven user interactions
- Modular component design
- localStorage API for data persistence

### Browser Compatibility
- Modern browsers with localStorage support
- Responsive design for desktop and mobile
- Progressive enhancement approach
- Graceful degradation for older browsers

## Getting Started

### Quick Start
1. Visit the live application
2. Try the demo account for immediate access with sample data
3. Create your own local account for personal use
4. Begin adding tasks and tracking your progress

### Demo Account
- Username: `demo`
- Password: `demo123`
- Pre-loaded with sample tasks, journal entries, and focus sessions
- Perfect for exploring features before creating your own account

## Development

### Local Development
```bash
# Clone the repository
git clone https://github.com/PrisDen/Sina.git
cd Sina

# Open in browser (no build process required)
open index.html
```

### Project Structure
```
Sina/
├── index.html          # Landing page
├── login.html          # Authentication
├── register.html       # Account creation
├── dashboard.html      # Main dashboard
├── tasks.html          # Task management
├── focus.html          # Pomodoro timer
├── journal.html        # Personal journaling
├── analytics.html      # Progress analytics
├── js/
│   └── sina-app.js     # Main application logic
├── netlify.toml        # Netlify configuration
├── _redirects          # URL routing
└── README.md           # Documentation
```

## Deployment

### Netlify Deployment
1. Connect your GitHub repository to Netlify
2. Set build command: (none required)
3. Set publish directory: `.` (root)
4. Deploy automatically on git push

### Configuration Files
- `netlify.toml` - Netlify-specific configuration
- `_redirects` - URL routing for single-page application behavior

## Philosophy

> "Discipline is the bridge between goals and accomplishment."

Sina embodies this philosophy through:
- **Consistent Structure** - Regular routines that build lasting habits
- **Adaptive Guidance** - Personalized feedback based on individual progress
- **Holistic Approach** - Combining task management, focus, reflection, and analytics
- **Long-term Vision** - Building sustainable discipline rather than quick fixes

## Contributing

We welcome contributions to improve Sina. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes with clear, descriptive commits
4. Test thoroughly across different browsers
5. Submit a pull request with detailed description

### Development Guidelines
- Maintain vanilla JavaScript approach (no frameworks)
- Ensure responsive design compatibility
- Follow existing code style and structure
- Test localStorage functionality thoroughly
- Update documentation for new features

## Legal and Compliance

### Licensing
This project is released under the MIT License. See [LICENSE](LICENSE) for details.

### Privacy Policy
Comprehensive privacy policy available at [PRIVACY.md](PRIVACY.md)

### Terms of Service
Full terms of service available at [TERMS.md](TERMS.md)

### Compliance
- GDPR compliant (no personal data collection)
- CCPA compliant (no data sharing)
- COPPA compliant (suitable for all ages)

## Support and Contact

### Documentation
- [Privacy Policy](PRIVACY.md)
- [Terms of Service](TERMS.md)
- [License](LICENSE)

### Issues and Feedback
For bug reports, feature requests, or general feedback:
- GitHub Issues: [https://github.com/PrisDen/Sina/issues](https://github.com/PrisDen/Sina/issues)
- Repository: [https://github.com/PrisDen/Sina](https://github.com/PrisDen/Sina)

## Acknowledgments

### Third-Party Services
- **Tailwind CSS** - Utility-first CSS framework
- **Font Awesome** - Icon library
- **Google Fonts** - Web typography
- **Netlify** - Static site hosting

### Inspiration
- **Pomodoro Technique** - Francesco Cirillo's time management method
- **Getting Things Done** - David Allen's productivity methodology
- **Atomic Habits** - James Clear's habit formation principles

---

**Start building unshakeable discipline today with Sina - Your Disciplined Mentor**

*Developed with dedication for those who choose discipline over regret.* 