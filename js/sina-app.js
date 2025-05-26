// Sina - Static Web Application
// localStorage-based implementation for GitHub Pages

class SinaApp {
    constructor() {
        this.currentUser = localStorage.getItem('sina_current_user');
        this.timer = new PomodoroTimer();
        this.notifications = new NotificationSystem();
        this.init();
    }

    init() {
        try {
            console.log('Sina App initializing...', {
                currentUser: this.currentUser,
                pathname: window.location.pathname
            });

            if (!this.currentUser) {
                // Redirect to login if not authenticated
                if (!window.location.pathname.includes('login.html') && 
                    !window.location.pathname.includes('register.html') && 
                    !window.location.pathname.includes('index.html')) {
                    console.log('No user logged in, redirecting to login');
                    window.location.href = 'login.html';
                    return;
                }
            }

            this.setupEventListeners();
            this.loadUserData();
            this.updateUI();
            this.startPeriodicUpdates();
            
            console.log('Sina App initialized successfully');
        } catch (error) {
            console.error('Error initializing Sina App:', error);
            this.notifications.show('Error loading application. Please refresh the page.', 'error');
        }
    }

    setupEventListeners() {
        // Navigation
        document.addEventListener('DOMContentLoaded', () => {
            this.animatePageLoad();
        });

        // Task management
        this.setupTaskHandlers();
        
        // Timer controls
        this.setupTimerHandlers();
        
        // Journal handlers
        this.setupJournalHandlers();
        
        // Logout handler
        const logoutBtn = document.querySelector('#logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', this.logout.bind(this));
        }
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

    setupTaskHandlers() {
        // Task completion checkboxes
        document.querySelectorAll('.task-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', this.handleTaskCompletion.bind(this));
        });

        // Add task buttons
        const addTaskBtns = document.querySelectorAll('[data-action="add-task"]');
        addTaskBtns.forEach(btn => {
            btn.addEventListener('click', this.showAddTaskModal.bind(this));
        });

        // Edit task buttons
        document.querySelectorAll('.edit-task-btn').forEach(button => {
            button.addEventListener('click', this.handleEditTask.bind(this));
        });

        // Delete task buttons
        document.querySelectorAll('.delete-task-btn').forEach(button => {
            button.addEventListener('click', this.handleDeleteTask.bind(this));
        });

        // Priority changes
        document.querySelectorAll('.priority-select').forEach(select => {
            select.addEventListener('change', this.handlePriorityChange.bind(this));
        });

        // Start focus session buttons
        document.querySelectorAll('.start-focus-btn').forEach(button => {
            button.addEventListener('click', this.handleStartFocus.bind(this));
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

    setupJournalHandlers() {
        const saveJournalBtn = document.querySelector('#save-journal-btn');
        if (saveJournalBtn) {
            saveJournalBtn.addEventListener('click', this.handleJournalSave.bind(this));
        }

        // Mood selection
        document.querySelectorAll('.mood-btn').forEach(btn => {
            btn.addEventListener('click', this.handleMoodSelection.bind(this));
        });
    }

    // Data Management
    loadUserData() {
        this.tasks = this.getTasks();
        this.journalEntries = this.getJournalEntries();
        this.focusSessions = this.getFocusSessions();
        
        // Initialize demo data if demo user and no data exists
        if (this.currentUser === 'demo' && this.tasks.length === 0) {
            this.initializeDemoData();
        }
    }

    initializeDemoData() {
        console.log('Initializing demo data...');
        
        // Demo tasks
        const demoTasks = [
            {
                id: 1,
                title: "Complete morning workout",
                description: "30-minute cardio session",
                priority: "high",
                category: "health",
                completed: true,
                created_at: new Date().toISOString(),
                completed_at: new Date().toISOString()
            },
            {
                id: 2,
                title: "Review project proposal",
                description: "Go through the Q4 project proposal and provide feedback",
                priority: "high",
                category: "work",
                completed: false,
                created_at: new Date().toISOString(),
                deadline: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString()
            },
            {
                id: 3,
                title: "Read 20 pages of book",
                description: "Continue reading 'Atomic Habits'",
                priority: "medium",
                category: "personal",
                completed: false,
                created_at: new Date().toISOString()
            }
        ];
        
        // Demo journal entries
        const demoJournal = [
            {
                id: Date.now(),
                content: "Started using Sina today. Feeling motivated to build better discipline habits. The interface is clean and the focus timer seems helpful.",
                mood: 4,
                created_at: new Date().toISOString()
            }
        ];
        
        // Demo focus sessions
        const demoSessions = [
            {
                id: Date.now(),
                task_id: 1,
                duration: 25,
                completed: true,
                notes: "Great focused session on workout planning",
                created_at: new Date(Date.now() - 60 * 60 * 1000).toISOString()
            }
        ];
        
        this.saveTasks(demoTasks);
        this.saveJournalEntries(demoJournal);
        this.saveFocusSessions(demoSessions);
        
        // Set task counter
        localStorage.setItem('sina_task_counter_demo', '3');
        
        console.log('Demo data initialized');
    }

    getTasks() {
        return JSON.parse(localStorage.getItem(`sina_tasks_${this.currentUser}`) || '[]');
    }

    saveTasks(tasks) {
        localStorage.setItem(`sina_tasks_${this.currentUser}`, JSON.stringify(tasks));
        this.tasks = tasks;
    }

    getJournalEntries() {
        return JSON.parse(localStorage.getItem(`sina_journal_${this.currentUser}`) || '[]');
    }

    saveJournalEntries(entries) {
        localStorage.setItem(`sina_journal_${this.currentUser}`, JSON.stringify(entries));
        this.journalEntries = entries;
    }

    getFocusSessions() {
        return JSON.parse(localStorage.getItem(`sina_focus_sessions_${this.currentUser}`) || '[]');
    }

    saveFocusSessions(sessions) {
        localStorage.setItem(`sina_focus_sessions_${this.currentUser}`, JSON.stringify(sessions));
        this.focusSessions = sessions;
    }

    getNextTaskId() {
        const counter = parseInt(localStorage.getItem(`sina_task_counter_${this.currentUser}`) || '0');
        const newCounter = counter + 1;
        localStorage.setItem(`sina_task_counter_${this.currentUser}`, newCounter.toString());
        return newCounter;
    }

    // Task Management
    handleTaskCompletion(event) {
        const checkbox = event.target;
        const taskId = parseInt(checkbox.dataset.taskId);
        const taskRow = checkbox.closest('.task-row');
        
        const tasks = this.getTasks();
        const task = tasks.find(t => t.id === taskId);
        
        if (task) {
            task.completed = checkbox.checked;
            task.completed_at = checkbox.checked ? new Date().toISOString() : null;
            this.saveTasks(tasks);
            
            if (checkbox.checked) {
                taskRow?.classList.add('task-completed');
                this.notifications.show('Task completed! Sina is proud of your progress.', 'success');
                this.showSinaReaction('task_completed');
            } else {
                taskRow?.classList.remove('task-completed');
            }
            
            this.updateDashboardStats();
        }
    }

    handlePriorityChange(event) {
        const select = event.target;
        const taskId = parseInt(select.dataset.taskId);
        const priority = select.value;
        
        const tasks = this.getTasks();
        const task = tasks.find(t => t.id === taskId);
        
        if (task) {
            task.priority = priority;
            this.saveTasks(tasks);
            this.notifications.show('Task priority updated.', 'info');
        }
    }

    handleEditTask(event) {
        const button = event.target.closest('button');
        const taskId = parseInt(button.dataset.taskId);
        this.showEditTaskModal(taskId);
    }

    handleDeleteTask(event) {
        const button = event.target.closest('button');
        const taskId = parseInt(button.dataset.taskId);
        
        if (confirm('Are you sure you want to delete this task?')) {
            const tasks = this.getTasks();
            const filteredTasks = tasks.filter(t => t.id !== taskId);
            this.saveTasks(filteredTasks);
            
            this.notifications.show('Task deleted.', 'info');
            this.refreshTaskList();
        }
    }

    handleStartFocus(event) {
        const button = event.target.closest('button');
        const taskId = parseInt(button.dataset.taskId);
        const taskTitle = button.dataset.taskTitle;
        
        this.startFocusSession(taskId, taskTitle);
    }

    showAddTaskModal() {
        const modal = this.createTaskModal();
        document.body.appendChild(modal);
    }

    showEditTaskModal(taskId) {
        const task = this.getTasks().find(t => t.id === taskId);
        if (!task) return;
        
        const modal = this.createTaskModal(task);
        document.body.appendChild(modal);
    }

    createTaskModal(task = null) {
        const isEdit = !!task;
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50';
        modal.innerHTML = `
            <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                <div class="mt-3">
                    <h3 class="text-lg font-medium text-gray-900 mb-4">
                        ${isEdit ? 'Edit Task' : 'Add New Task'}
                    </h3>
                    <form id="task-form">
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Title</label>
                            <input type="text" name="title" required value="${task?.title || ''}"
                                   class="w-full p-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
                            <textarea name="description" rows="3" 
                                      class="w-full p-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500">${task?.description || ''}</textarea>
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                            <select name="priority" class="w-full p-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500">
                                <option value="low" ${task?.priority === 'low' ? 'selected' : ''}>Low</option>
                                <option value="medium" ${task?.priority === 'medium' ? 'selected' : ''}>Medium</option>
                                <option value="high" ${task?.priority === 'high' ? 'selected' : ''}>High</option>
                            </select>
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
                            <select name="category" class="w-full p-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500">
                                <option value="personal" ${task?.category === 'personal' ? 'selected' : ''}>Personal</option>
                                <option value="work" ${task?.category === 'work' ? 'selected' : ''}>Work</option>
                                <option value="study" ${task?.category === 'study' ? 'selected' : ''}>Study</option>
                                <option value="health" ${task?.category === 'health' ? 'selected' : ''}>Health</option>
                            </select>
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Deadline (optional)</label>
                            <input type="datetime-local" name="deadline" value="${task?.deadline ? new Date(task.deadline).toISOString().slice(0, 16) : ''}"
                                   class="w-full p-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500">
                        </div>
                        <div class="flex justify-end space-x-3">
                            <button type="button" class="cancel-btn px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400">Cancel</button>
                            <button type="submit" class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700">
                                ${isEdit ? 'Update Task' : 'Add Task'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        
        // Handle form submission
        modal.querySelector('#task-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitTask(e.target, task);
            document.body.removeChild(modal);
        });
        
        // Handle cancel
        modal.querySelector('.cancel-btn').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        // Close on backdrop click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
        
        return modal;
    }

    submitTask(form, existingTask = null) {
        const formData = new FormData(form);
        const taskData = {
            title: formData.get('title'),
            description: formData.get('description'),
            priority: formData.get('priority'),
            category: formData.get('category'),
            deadline: formData.get('deadline') || null,
            completed: existingTask?.completed || false,
            created_at: existingTask?.created_at || new Date().toISOString(),
            updated_at: new Date().toISOString()
        };
        
        const tasks = this.getTasks();
        
        if (existingTask) {
            // Update existing task
            const index = tasks.findIndex(t => t.id === existingTask.id);
            if (index !== -1) {
                tasks[index] = { ...existingTask, ...taskData };
                this.notifications.show('Task updated successfully!', 'success');
            }
        } else {
            // Create new task
            taskData.id = this.getNextTaskId();
            tasks.push(taskData);
            this.notifications.show('Task created! Sina is ready to help you complete it.', 'success');
        }
        
        this.saveTasks(tasks);
        this.refreshTaskList();
        this.updateDashboardStats();
    }

    // Journal Management
    handleJournalSave(event) {
        event.preventDefault();
        const textarea = document.querySelector('#journal-content') || document.querySelector('#journal-textarea');
        const content = textarea?.value;
        const selectedMood = document.querySelector('.mood-btn.selected')?.dataset.mood;
        
        if (!content || content.trim().length < 10) {
            this.notifications.show('Sina encourages more thoughtful reflection. Write at least 10 characters.', 'error');
            return;
        }
        
        const journalEntry = {
            id: Date.now(),
            content: content.trim(),
            mood: selectedMood ? parseInt(selectedMood) : 3,
            created_at: new Date().toISOString()
        };
        
        const entries = this.getJournalEntries();
        entries.unshift(journalEntry);
        this.saveJournalEntries(entries);
        
        this.notifications.show('Journal entry saved. Sina appreciates your reflection.', 'success');
        
        // Clear form
        if (textarea) textarea.value = '';
        document.querySelectorAll('.mood-btn').forEach(btn => btn.classList.remove('selected'));
        
        this.refreshJournalList();
    }

    handleMoodSelection(event) {
        document.querySelectorAll('.mood-btn').forEach(btn => btn.classList.remove('selected'));
        event.target.classList.add('selected');
    }

    // Focus Session Management
    startFocusSession(taskId, taskTitle) {
        this.timer.setTaskContext(taskId, taskTitle);
        this.timer.start();
        
        // Navigate to focus page if not already there
        if (!window.location.pathname.includes('focus.html')) {
            window.location.href = 'focus.html';
        }
    }

    logFocusSession(taskId, duration, notes = '') {
        const session = {
            id: Date.now(),
            task_id: taskId,
            duration: duration,
            completed: true,
            notes: notes,
            created_at: new Date().toISOString()
        };
        
        const sessions = this.getFocusSessions();
        sessions.unshift(session);
        this.saveFocusSessions(sessions);
        
        this.showSinaReaction('session_completed');
    }

    // UI Updates
    updateUI() {
        this.updateDashboardStats();
        this.updateSinaMessage();
        this.refreshTaskList();
        this.refreshJournalList();
    }

    updateDashboardStats() {
        const tasks = this.getTasks();
        const today = new Date().toDateString();
        const todayTasks = tasks.filter(t => new Date(t.created_at).toDateString() === today);
        const completedToday = todayTasks.filter(t => t.completed).length;
        
        // Update stats in dashboard
        const taskProgressElement = document.querySelector('[data-stat="task-progress"]');
        if (taskProgressElement) {
            taskProgressElement.textContent = `${completedToday}/${todayTasks.length}`;
        }
        
        const progressBar = document.querySelector('[data-element="progress-bar"]');
        if (progressBar && todayTasks.length > 0) {
            const percentage = (completedToday / todayTasks.length) * 100;
            progressBar.style.width = `${percentage}%`;
        }
        
        const percentageText = document.querySelector('[data-stat="completion-percentage"]');
        if (percentageText && todayTasks.length > 0) {
            const percentage = Math.round((completedToday / todayTasks.length) * 100);
            percentageText.textContent = `${percentage}% complete`;
        }
        
        // Update other stats
        const totalTasksElement = document.querySelector('[data-stat="total-tasks"]');
        if (totalTasksElement) {
            totalTasksElement.textContent = tasks.length.toString();
        }
        
        const completedTasksElement = document.querySelector('[data-stat="completed-tasks"]');
        if (completedTasksElement) {
            completedTasksElement.textContent = tasks.filter(t => t.completed).length.toString();
        }
        
        const focusSessionsElement = document.querySelector('[data-stat="focus-sessions"]');
        if (focusSessionsElement) {
            focusSessionsElement.textContent = this.getFocusSessions().length.toString();
        }
    }

    updateSinaMessage() {
        const messageElement = document.querySelector('[data-element="sina-message"]');
        if (!messageElement) return;
        
        const performance = this.calculateWeeklyPerformance();
        const message = this.getSinaMessage(performance);
        
        messageElement.innerHTML = `
            <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                    <i class="fas fa-brain text-2xl text-purple-600"></i>
                </div>
                <div>
                    <p class="text-gray-800 font-medium">${message.text}</p>
                    <p class="text-sm text-gray-600 mt-1">${message.quote}</p>
                </div>
            </div>
        `;
    }

    calculateWeeklyPerformance() {
        const tasks = this.getTasks();
        const oneWeekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
        const weeklyTasks = tasks.filter(t => new Date(t.created_at) >= oneWeekAgo);
        const completedWeekly = weeklyTasks.filter(t => t.completed).length;
        
        if (weeklyTasks.length === 0) return 0;
        return completedWeekly / weeklyTasks.length;
    }

    getSinaMessage(performance) {
        if (performance >= 0.8) {
            return {
                text: "Outstanding work! Your discipline is truly impressive.",
                quote: "Excellence is not an act, but a habit. You're living proof of this."
            };
        } else if (performance >= 0.6) {
            return {
                text: "Good progress! Keep building that momentum.",
                quote: "Success is the sum of small efforts repeated day in and day out."
            };
        } else if (performance >= 0.4) {
            return {
                text: "You're on the right path. Let's focus on consistency.",
                quote: "Discipline is choosing between what you want now and what you want most."
            };
        } else {
            return {
                text: "Time to refocus. I believe in your potential.",
                quote: "The pain of discipline weighs ounces, but the pain of regret weighs tons."
            };
        }
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
            ]
        };
        
        const messages = reactions[event] || reactions['task_completed'];
        const message = messages[Math.floor(Math.random() * messages.length)];
        
        this.notifications.show(`Sina says: "${message}"`, 'success');
    }

    refreshTaskList() {
        // This would be implemented based on the specific page
        if (window.location.pathname.includes('tasks.html')) {
            this.renderTasksPage();
        } else if (window.location.pathname.includes('dashboard.html')) {
            this.renderDashboardTasks();
        }
    }

    refreshJournalList() {
        if (window.location.pathname.includes('journal.html')) {
            this.renderJournalPage();
        }
    }

    renderTasksPage() {
        // Placeholder for tasks page rendering
        console.log('Tasks page rendering - implement based on HTML structure');
    }

    renderDashboardTasks() {
        // Placeholder for dashboard tasks rendering
        console.log('Dashboard tasks rendering - implement based on HTML structure');
    }

    renderJournalPage() {
        // Placeholder for journal page rendering
        console.log('Journal page rendering - implement based on HTML structure');
    }

    // Utility Methods
    logout() {
        localStorage.removeItem('sina_current_user');
        window.location.href = 'index.html';
    }

    startPeriodicUpdates() {
        // Update stats every 5 minutes
        setInterval(() => {
            this.updateDashboardStats();
        }, 5 * 60 * 1000);
        
        // Update Sina's message every 30 minutes
        setInterval(() => {
            this.updateSinaMessage();
        }, 30 * 60 * 1000);
    }
}

// Pomodoro Timer Class
class PomodoroTimer {
    constructor() {
        this.duration = 25 * 60; // 25 minutes in seconds
        this.timeLeft = this.duration;
        this.isRunning = false;
        this.interval = null;
        this.taskId = null;
        this.taskTitle = '';
    }

    setTaskContext(taskId, taskTitle) {
        this.taskId = taskId;
        this.taskTitle = taskTitle;
    }

    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.interval = setInterval(() => {
            this.timeLeft--;
            this.updateDisplay();
            
            if (this.timeLeft <= 0) {
                this.complete();
            }
        }, 1000);
        
        this.updateTimerState('running');
    }

    pause() {
        this.isRunning = false;
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
        this.updateTimerState('paused');
    }

    reset() {
        this.pause();
        this.timeLeft = this.duration;
        this.updateDisplay();
        this.updateTimerState('stopped');
    }

    complete() {
        this.pause();
        this.updateTimerState('completed');
        
        // Log the session
        if (this.taskId && window.sinaApp) {
            window.sinaApp.logFocusSession(this.taskId, this.duration / 60);
        }
        
        // Show completion notification
        if (window.sinaApp) {
            window.sinaApp.notifications.show('Focus session completed! Take a well-deserved break.', 'success');
        }
        
        this.reset();
    }

    updateDisplay() {
        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;
        const display = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        const timerDisplay = document.querySelector('[data-element="timer-display"]');
        if (timerDisplay) {
            timerDisplay.textContent = display;
        }
        
        // Update page title
        if (this.isRunning) {
            document.title = `${display} - Focus Session - Sina`;
        }
    }

    updateTimerState(state) {
        const startBtn = document.querySelector('#start-timer');
        const pauseBtn = document.querySelector('#pause-timer');
        const resetBtn = document.querySelector('#reset-timer');
        
        if (startBtn) startBtn.style.display = state === 'running' ? 'none' : 'inline-block';
        if (pauseBtn) pauseBtn.style.display = state === 'running' ? 'inline-block' : 'none';
        if (resetBtn) resetBtn.disabled = state === 'stopped';
    }
}

// Notification System
class NotificationSystem {
    show(message, type = 'info', duration = 5000) {
        const container = this.getContainer();
        const notification = document.createElement('div');
        
        const bgColor = {
            'success': 'bg-green-500',
            'error': 'bg-red-500',
            'info': 'bg-blue-500',
            'warning': 'bg-yellow-500'
        }[type] || 'bg-blue-500';
        
        notification.className = `${bgColor} text-white px-6 py-3 rounded-lg shadow-lg mb-2 transform translate-x-full transition-transform duration-300`;
        notification.innerHTML = `
            <div class="flex items-center justify-between">
                <div class="flex items-center">
                    <i class="fas fa-${this.getIcon(type)} mr-2"></i>
                    <span>${message}</span>
                </div>
                <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentNode.parentNode.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        container.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Auto remove
        setTimeout(() => {
            if (notification.parentNode) {
                notification.classList.add('translate-x-full');
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }
        }, duration);
    }

    getContainer() {
        let container = document.getElementById('notification-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notification-container';
            container.className = 'fixed top-4 right-4 z-50';
            document.body.appendChild(container);
        }
        return container;
    }

    getIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-triangle',
            'info': 'info-circle',
            'warning': 'exclamation-circle'
        };
        return icons[type] || 'info-circle';
    }
}

// Authentication functions
function handleLogin(event) {
    event.preventDefault();
    const form = event.target;
    const username = form.username.value;
    const password = form.password.value;
    
    console.log('Login attempt:', { username });
    
    // Demo account
    if (username === 'demo' && password === 'demo123') {
        localStorage.setItem('sina_current_user', 'demo');
        window.location.href = 'dashboard.html';
        return;
    }
    
    // Check if user exists
    const users = JSON.parse(localStorage.getItem('sina_users') || '{}');
    if (users[username] && users[username].password === password) {
        localStorage.setItem('sina_current_user', username);
        window.location.href = 'dashboard.html';
    } else {
        alert('Invalid username or password');
    }
}

function handleRegister(event) {
    event.preventDefault();
    const form = event.target;
    const username = form.username.value;
    const password = form.password.value;
    const confirmPassword = form.confirmPassword?.value;
    
    console.log('Register attempt:', { username });
    
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }
    
    if (password.length < 6) {
        alert('Password must be at least 6 characters');
        return;
    }
    
    const users = JSON.parse(localStorage.getItem('sina_users') || '{}');
    if (users[username]) {
        alert('Username already exists');
        return;
    }
    
    users[username] = { password: password, created_at: new Date().toISOString() };
    localStorage.setItem('sina_users', JSON.stringify(users));
    localStorage.setItem('sina_current_user', username);
    
    window.location.href = 'dashboard.html';
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Setup authentication forms
    const loginForm = document.querySelector('#login-form');
    const registerForm = document.querySelector('#register-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    // Initialize main app
    window.sinaApp = new SinaApp();
});

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SinaApp, PomodoroTimer, NotificationSystem };
} 