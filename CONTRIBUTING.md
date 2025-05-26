# Contributing to Sina

Thank you for your interest in contributing to Sina - Your Disciplined Mentor. This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Issues

Before creating an issue, please:
1. Check existing issues to avoid duplicates
2. Use the issue template if available
3. Provide clear, detailed information about the problem
4. Include steps to reproduce the issue
5. Specify browser and operating system details

### Suggesting Features

When suggesting new features:
1. Explain the use case and benefit
2. Consider how it fits with Sina's philosophy of discipline building
3. Provide mockups or detailed descriptions if applicable
4. Discuss potential implementation approaches

### Pull Requests

#### Before You Start
1. Fork the repository
2. Create a feature branch from `master`
3. Ensure your local environment is set up correctly

#### Development Guidelines

##### Code Style
- Use consistent indentation (2 spaces for HTML/CSS, 4 spaces for JavaScript)
- Follow existing naming conventions
- Write clear, descriptive variable and function names
- Add comments for complex logic

##### JavaScript Guidelines
- Maintain the vanilla JavaScript approach (no frameworks)
- Use ES6+ features where appropriate
- Follow object-oriented patterns established in the codebase
- Ensure localStorage operations are safe and error-handled

##### HTML/CSS Guidelines
- Use semantic HTML5 elements
- Maintain responsive design principles
- Follow Tailwind CSS utility classes where possible
- Ensure accessibility standards (ARIA labels, keyboard navigation)

##### Testing
- Test functionality across major browsers (Chrome, Firefox, Safari, Edge)
- Verify responsive design on different screen sizes
- Test localStorage functionality thoroughly
- Ensure no data leakage or privacy issues

#### Pull Request Process

1. **Create a descriptive branch name**
   ```bash
   git checkout -b feature/task-filtering
   git checkout -b fix/timer-reset-bug
   git checkout -b docs/update-readme
   ```

2. **Make your changes**
   - Keep commits focused and atomic
   - Write clear commit messages
   - Test thoroughly before committing

3. **Update documentation**
   - Update README.md if adding new features
   - Add or update code comments
   - Update any relevant documentation files

4. **Submit the pull request**
   - Use the pull request template
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes

5. **Respond to feedback**
   - Address review comments promptly
   - Make requested changes in additional commits
   - Keep the conversation constructive

## Development Setup

### Prerequisites
- Modern web browser with localStorage support
- Text editor or IDE
- Git for version control

### Local Development
```bash
# Clone your fork
git clone https://github.com/yourusername/Sina.git
cd Sina

# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes and test
# Open index.html in your browser

# Commit your changes
git add .
git commit -m "Add descriptive commit message"

# Push to your fork
git push origin feature/your-feature-name
```

### Testing Checklist
- [ ] Application loads without errors
- [ ] All navigation links work correctly
- [ ] Task creation, editing, and deletion function properly
- [ ] Timer starts, pauses, and resets correctly
- [ ] Journal entries save and display properly
- [ ] Data persists after browser refresh
- [ ] Responsive design works on mobile devices
- [ ] No console errors in browser developer tools

## Project Structure

### Key Files
- `index.html` - Landing page and entry point
- `js/sina-app.js` - Main application logic
- `dashboard.html` - Primary user interface
- `tasks.html` - Task management interface
- `focus.html` - Pomodoro timer interface
- `journal.html` - Journaling interface
- `netlify.toml` - Deployment configuration

### Data Architecture
- All user data stored in browser localStorage
- No server-side database or API
- JSON format for data serialization
- User-specific data keys for multi-user support

## Feature Development Guidelines

### Sina's Personality System
When working on Sina's adaptive messaging:
- Maintain the three personality modes (encouraging, motivational, strict)
- Base personality changes on user performance metrics
- Keep messages supportive but honest
- Avoid overly casual or unprofessional language

### User Interface
- Maintain the purple gradient theme
- Use Tailwind CSS utilities consistently
- Ensure accessibility compliance
- Keep interfaces clean and uncluttered

### Data Privacy
- Never transmit user data to external services
- Maintain localStorage-only architecture
- Respect user privacy in all features
- Document any external service dependencies

## Release Process

### Version Numbering
We follow semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes or major feature additions
- MINOR: New features that are backward compatible
- PATCH: Bug fixes and minor improvements

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version number incremented
- [ ] No breaking changes in minor/patch releases

## Getting Help

### Resources
- [README.md](README.md) - Project overview and setup
- [PRIVACY.md](PRIVACY.md) - Privacy policy and data handling
- [TERMS.md](TERMS.md) - Terms of service
- [GitHub Issues](https://github.com/PrisDen/Sina/issues) - Bug reports and feature requests

### Communication
- Use GitHub Issues for bug reports and feature requests
- Keep discussions focused and constructive
- Provide context and examples when asking questions
- Be patient and respectful with maintainers and other contributors

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes for significant contributions
- README acknowledgments for major features

Thank you for helping make Sina better for everyone who chooses discipline over regret! 