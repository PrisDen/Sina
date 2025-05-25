// Sina - Main JavaScript Application

class SinaApp {
    constructor() {
        this.timer = new PomodoroTimer();
        this.notifications = new NotificationSystem();
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadUserPreferences();
        this.startPeriodicUpdates();
    }

    setupEventListeners() {
        // Navigation
        document.addEventListener('DOMContentLoaded', () => {
            this.animatePageLoad();
        });

        // Form submissions
        this.setupFormHandlers();
        
        // Task interactions
        this.setupTaskHandlers();
        
        // Timer controls
        this.setupTimerHandlers();
    }

    animatePageLoad() {
        const elements = document.querySelectorAll('.fade-in');
        elements.forEach((el, index) => {
            setTimeout(() => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    setupFormHandlers() {
        // Login form
        const loginForm = document.querySelector('#login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', this.handleLogin.bind(this));
        }

        // Registration form
        const registerForm = document.querySelector('#register-form');
        if (registerForm) {
            registerForm.addEventListener('submit', this.handleRegistration.bind(this));
        }

        // Journal form
        const journalForm = document.querySelector('#journal-form');
        if (journalForm) {
            journalForm.addEventListener('submit', this.handleJournalEntry.bind(this));
        }
    }

    setupTaskHandlers() {
        // Task completion checkboxes
        document.querySelectorAll('.task-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', this.handleTaskCompletion.bind(this));
        });

        // Add task buttons
        const addTaskBtn = document.querySelector('#add-task-btn');
        const addFirstTaskBtn = document.querySelector('#add-first-task-btn');
        
        if (addTaskBtn) {
            addTaskBtn.addEventListener('click', this.showAddTaskModal.bind(this));
        }
        
        if (addFirstTaskBtn) {
            addFirstTaskBtn.addEventListener('click', this.showAddTaskModal.bind(this));
        }

        // Quick action buttons
        document.querySelectorAll('button').forEach(button => {
            if (button.textContent.includes('Add New Task')) {
                button.addEventListener('click', this.showAddTaskModal.bind(this));
            }
        });

        // Journal save button
        const saveJournalBtn = document.querySelector('#save-journal-btn');
        if (saveJournalBtn) {
            saveJournalBtn.addEventListener('click', this.handleJournalSave.bind(this));
        }

        // Task priority changes
        document.querySelectorAll('.priority-select').forEach(select => {
            select.addEventListener('change', this.handlePriorityChange.bind(this));
        });
    }

    setupTimerHandlers() {
        const startBtn = document.querySelector('#start-timer');
        const pauseBtn = document.querySelector('#pause-timer');
        const resetBtn = document.querySelector('#reset-timer');

        if (startBtn) startBtn.addEventListener('click', () => this.timer.start());
        if (pauseBtn) pauseBtn.addEventListener('click', () => this.timer.pause());
        if (resetBtn) resetBtn.addEventListener('click', () => this.timer.reset());
    }

    handleLogin(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        
        // Add loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.classList.add('loading');
        
        // Submit form (handled by Flask backend)
        form.submit();
    }

    handleRegistration(event) {
        event.preventDefault();
        const form = event.target;
        const password = form.querySelector('#password').value;
        const confirmPassword = form.querySelector('#confirm_password').value;
        
        if (password !== confirmPassword) {
            this.notifications.show('Passwords do not match. Sina values consistency.', 'error');
            return;
        }
        
        if (password.length < 6) {
            this.notifications.show('Password must be at least 6 characters. Security matters.', 'error');
            return;
        }
        
        form.submit();
    }

    handleTaskCompletion(event) {
        const checkbox = event.target;
        const taskRow = checkbox.closest('.task-row');
        const taskId = checkbox.dataset.taskId;
        
        if (checkbox.checked) {
            taskRow.classList.add('task-completed');
            this.completeTask(taskId);
            this.notifications.show('Task completed! Sina is proud of your progress.', 'success');
        } else {
            taskRow.classList.remove('task-completed');
            this.uncompleteTask(taskId);
        }
    }

    handleJournalEntry(event) {
        event.preventDefault();
        const form = event.target;
        const content = form.querySelector('textarea').value;
        
        if (content.trim().length < 10) {
            this.notifications.show('Sina encourages more thoughtful reflection. Write at least 10 characters.', 'error');
            return;
        }
        
        this.saveJournalEntry(content);
    }

    handleJournalSave(event) {
        event.preventDefault();
        const textarea = document.querySelector('#journal-textarea');
        const content = textarea.value;
        
        if (content.trim().length < 10) {
            this.notifications.show('Sina encourages more thoughtful reflection. Write at least 10 characters.', 'error');
            return;
        }
        
        this.saveJournalEntry(content);
    }

    handlePriorityChange(event) {
        const select = event.target;
        const taskId = select.dataset.taskId;
        const priority = select.value;
        
        this.updateTaskPriority(taskId, priority);
    }

    completeTask(taskId) {
        fetch('/api/tasks/complete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task_id: taskId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.updateDashboardStats();
                this.showSinaReaction('task_completed');
            }
        })
        .catch(error => {
            console.error('Error completing task:', error);
            this.notifications.show('Failed to complete task. Try again.', 'error');
        });
    }

    uncompleteTask(taskId) {
        fetch('/api/tasks/uncomplete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task_id: taskId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.updateDashboardStats();
            }
        });
    }

    saveJournalEntry(content) {
        fetch('/api/journal/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: content })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.notifications.show('Journal entry saved. Sina appreciates your reflection.', 'success');
                const textarea = document.querySelector('#journal-textarea');
                if (textarea) {
                    textarea.value = '';
                }
            }
        })
        .catch(error => {
            console.error('Error saving journal:', error);
            this.notifications.show('Failed to save journal entry.', 'error');
        });
    }

    updateTaskPriority(taskId, priority) {
        fetch('/api/tasks/priority', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task_id: taskId, priority: priority })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.notifications.show('Task priority updated.', 'info');
            }
        });
    }

    updateDashboardStats() {
        fetch('/api/dashboard/stats')
        .then(response => response.json())
        .then(data => {
            // Update stats on dashboard
            document.querySelector('#today-tasks').textContent = `${data.completed_today}/${data.today_tasks}`;
            document.querySelector('#today-minutes').textContent = `${data.today_minutes} min`;
            document.querySelector('#current-streak').textContent = `${data.streak} days`;
            
            // Update progress bar
            const progressBar = document.querySelector('.progress-bar');
            if (progressBar && data.today_tasks > 0) {
                const percentage = (data.completed_today / data.today_tasks) * 100;
                progressBar.style.width = `${percentage}%`;
            }
        });
    }

    showSinaReaction(event) {
        const reactions = {
            'task_completed': [
                'Excellent work! Keep building that momentum.',
                'Another step closer to your goals. I\'m proud.',
                'Discipline in action. This is how success is built.'
            ],
            'session_completed': [
                'Focused work pays off. Well done.',
                'That\'s the kind of dedication I like to see.',
                'Your future self will thank you for this session.'
            ],
            'streak_milestone': [
                'Outstanding! Your consistency is impressive.',
                'This streak shows real commitment. Keep going!',
                'You\'re building unshakeable discipline.'
            ]
        };
        
        const messages = reactions[event] || reactions['task_completed'];
        const message = messages[Math.floor(Math.random() * messages.length)];
        
        this.notifications.show(`Sina says: "${message}"`, 'success');
    }

    showAddTaskModal() {
        // Create modal HTML
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50';
        modal.innerHTML = `
            <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                <div class="mt-3">
                    <h3 class="text-lg font-medium text-gray-900 mb-4">Add New Task</h3>
                    <form id="add-task-form">
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Title</label>
                            <input type="text" name="title" required class="w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
                            <textarea name="description" rows="3" class="w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"></textarea>
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                            <select name="priority" class="w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500">
                                <option value="low">Low</option>
                                <option value="medium" selected>Medium</option>
                                <option value="high">High</option>
                            </select>
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
                            <select name="category" class="w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500">
                                <option value="personal">Personal</option>
                                <option value="work">Work</option>
                                <option value="study">Study</option>
                                <option value="health">Health</option>
                            </select>
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Deadline (optional)</label>
                            <input type="datetime-local" name="deadline" class="w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500">
                        </div>
                        <div class="flex justify-end space-x-3">
                            <button type="button" id="cancel-task" class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400">Cancel</button>
                            <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">Add Task</button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Handle form submission
        modal.querySelector('#add-task-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitNewTask(e.target);
            document.body.removeChild(modal);
        });
        
        // Handle cancel
        modal.querySelector('#cancel-task').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        // Close on backdrop click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
    }

    submitNewTask(form) {
        const formData = new FormData(form);
        const taskData = Object.fromEntries(formData);
        
        fetch('/api/tasks/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.notifications.show('Task created! Sina is ready to help you complete it.', 'success');
                location.reload(); // Refresh to show new task
            } else {
                this.notifications.show('Failed to create task. Try again.', 'error');
            }
        })
        .catch(error => {
            console.error('Error creating task:', error);
            this.notifications.show('Failed to create task.', 'error');
        });
    }

    loadUserPreferences() {
        // Load user settings from localStorage or API
        const preferences = localStorage.getItem('sina_preferences');
        if (preferences) {
            const prefs = JSON.parse(preferences);
            this.applyPreferences(prefs);
        }
    }

    applyPreferences(prefs) {
        if (prefs.darkMode) {
            document.body.classList.add('dark-mode');
        }
        
        if (prefs.timerDuration) {
            this.timer.setDuration(prefs.timerDuration);
        }
    }

    startPeriodicUpdates() {
        // Update dashboard stats every 5 minutes
        setInterval(() => {
            this.updateDashboardStats();
        }, 5 * 60 * 1000);
        
        // Check for motivational reminders every hour
        setInterval(() => {
            this.checkForReminders();
        }, 60 * 60 * 1000);
    }

    checkForReminders() {
        const lastActivity = localStorage.getItem('sina_last_activity');
        const now = Date.now();
        
        if (!lastActivity || (now - parseInt(lastActivity)) > 2 * 60 * 60 * 1000) {
            this.notifications.show('Sina reminds you: Discipline is a daily choice. What will you accomplish today?', 'info');
        }
    }
}

// Pomodoro Timer Class
class PomodoroTimer {
    constructor() {
        this.duration = 25 * 60; // 25 minutes
        this.timeLeft = this.duration;
        this.isRunning = false;
        this.interval = null;
        this.display = document.getElementById('timer-display');
    }

    start() {
        if (!this.isRunning) {
            this.isRunning = true;
            this.interval = setInterval(() => {
                this.timeLeft--;
                this.updateDisplay();
                
                if (this.timeLeft <= 0) {
                    this.complete();
                }
            }, 1000);
            
            this.updateTimerState('active');
        }
    }

    pause() {
        if (this.isRunning) {
            clearInterval(this.interval);
            this.isRunning = false;
            this.updateTimerState('paused');
        }
    }

    reset() {
        clearInterval(this.interval);
        this.isRunning = false;
        this.timeLeft = this.duration;
        this.updateDisplay();
        this.updateTimerState('reset');
    }

    complete() {
        clearInterval(this.interval);
        this.isRunning = false;
        
        // Show completion notification
        const notification = new NotificationSystem();
        notification.show('Focus session complete! Time for a break. Sina is proud of your dedication.', 'success');
        
        // Log the session
        this.logSession();
        
        // Reset timer
        this.timeLeft = this.duration;
        this.updateDisplay();
        this.updateTimerState('reset');
    }

    updateDisplay() {
        if (this.display) {
            const minutes = Math.floor(this.timeLeft / 60);
            const seconds = this.timeLeft % 60;
            this.display.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
    }

    updateTimerState(state) {
        const timerCard = document.querySelector('.timer-card');
        if (timerCard) {
            timerCard.classList.remove('timer-active', 'timer-paused');
            if (state === 'active') {
                timerCard.classList.add('timer-active');
            } else if (state === 'paused') {
                timerCard.classList.add('timer-paused');
            }
        }
    }

    logSession() {
        const sessionData = {
            duration: Math.floor((this.duration - this.timeLeft) / 60),
            completed: this.timeLeft === 0
        };
        
        fetch('/api/sessions/log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(sessionData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update session count on dashboard
                const sessionCount = document.querySelector('#today-sessions');
                if (sessionCount) {
                    const current = parseInt(sessionCount.textContent) || 0;
                    sessionCount.textContent = current + 1;
                }
            }
        });
    }

    setDuration(minutes) {
        this.duration = minutes * 60;
        this.timeLeft = this.duration;
        this.updateDisplay();
    }
}

// Notification System Class
class NotificationSystem {
    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    <i class="fas ${this.getIcon(type)}"></i>
                </div>
                <div class="ml-3">
                    <p class="text-sm font-medium">${message}</p>
                </div>
                <div class="ml-auto pl-3">
                    <button class="text-white hover:text-gray-200" onclick="this.parentElement.parentElement.parentElement.remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after duration
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, duration);
    }

    getIcon(type) {
        const icons = {
            'success': 'fa-check-circle',
            'error': 'fa-exclamation-circle',
            'info': 'fa-info-circle',
            'warning': 'fa-exclamation-triangle'
        };
        return icons[type] || icons['info'];
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.sinaApp = new SinaApp();
    
    // Update last activity timestamp
    localStorage.setItem('sina_last_activity', Date.now().toString());
}); 