// API Base URL - automatically detect if running locally or on GitHub Pages
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:3000/api'
    : 'DEMO_MODE'; // Use demo mode for GitHub Pages

// Global state
let currentNextTaskId = null;
let currentFilter = 'all';
let demoTasks = [];
let demoNextId = 1;

// Demo mode helper to check if using demo
function isDemoMode() {
    return API_URL === 'DEMO_MODE';
}

// Initialize demo tasks
function initDemoTasks() {
    demoTasks = [
        {
            id: 1,
            title: "Complete project proposal",
            description: "Finish Q4 project proposal for client",
            urgency: 9,
            importance: 10,
            estimatedEffort: 3,
            deadline: new Date(Date.now() + 4 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            dependencies: [],
            completed: false,
            createdAt: new Date().toISOString(),
            priorityScore: 80.5,
            daysUntilDeadline: 4,
            isBlocked: false
        },
        {
            id: 2,
            title: "Review code PRs",
            description: "Review 3 pending pull requests",
            urgency: 7,
            importance: 6,
            estimatedEffort: 1,
            deadline: new Date(Date.now() + 1 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            dependencies: [],
            completed: false,
            createdAt: new Date().toISOString(),
            priorityScore: 73.5,
            daysUntilDeadline: 1,
            isBlocked: false
        }
    ];
    demoNextId = 3;
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    if (isDemoMode()) {
        initDemoTasks();
        showDemoNotification();
    }
    loadStats();
    loadTasks();
    setupFormSubmit();
    setupRatingButtons();
    setupDeadlineButtons();
});

// Show demo notification
function showDemoNotification() {
    const banner = document.getElementById('demoBanner');
    if (banner) {
        banner.style.display = 'flex';
        banner.style.justifyContent = 'center';
        banner.style.alignItems = 'center';
    }
}

// Load statistics
async function loadStats() {
    try {
        if (isDemoMode()) {
            const completedTasks = demoTasks.filter(t => t.completed).length;
            const incompleteTasks = demoTasks.filter(t => !t.completed).length;
            const highPriorityTasks = demoTasks.filter(t => !t.completed && t.priorityScore > 70).length;
            
            document.getElementById('totalTasks').textContent = demoTasks.length;
            document.getElementById('completedTasks').textContent = completedTasks;
            document.getElementById('incompleteTasks').textContent = incompleteTasks;
            document.getElementById('highPriorityTasks').textContent = highPriorityTasks;
            return;
        }
        
        const response = await fetch(`${API_URL}/stats`);
        const data = await response.json();
        
        document.getElementById('totalTasks').textContent = data.totalTasks;
        document.getElementById('completedTasks').textContent = data.completedTasks;
        document.getElementById('incompleteTasks').textContent = data.incompleteTasks;
        document.getElementById('highPriorityTasks').textContent = data.highPriorityTasks;
    } catch (error) {
        console.error('Error loading stats:', error);
        document.getElementById('totalTasks').textContent = '0';
        document.getElementById('completedTasks').textContent = '0';
        document.getElementById('incompleteTasks').textContent = '0';
        document.getElementById('highPriorityTasks').textContent = '0';
    }
}

// Get next recommended task
async function getNextTask() {
    try {
        const response = await fetch(`${API_URL}/tasks/next`);
        const data = await response.json();
        
        const nextTaskCard = document.getElementById('nextTaskCard');
        
        if (data.task) {
            currentNextTaskId = data.task.id;
            
            document.getElementById('nextTaskTitle').textContent = data.task.title;
            document.getElementById('nextTaskDescription').textContent = data.task.description || 'No description provided';
            document.getElementById('nextTaskPriority').textContent = `Priority: ${data.task.priorityScore}`;
            document.getElementById('nextTaskDeadline').textContent = data.task.deadline 
                ? `${data.task.daysUntilDeadline} days until ${new Date(data.task.deadline).toLocaleDateString()}`
                : 'No deadline';
            document.getElementById('nextTaskEffort').textContent = data.task.estimatedEffort;
            document.getElementById('nextTaskUrgency').textContent = data.task.urgency;
            document.getElementById('nextTaskImportance').textContent = data.task.importance;
            
            nextTaskCard.classList.remove('hidden');
        } else {
            alert(data.message || 'No tasks available!');
            nextTaskCard.classList.add('hidden');
        }
    } catch (error) {
        console.error('Error getting next task:', error);
        alert('Failed to get next task. Make sure the API is running.');
    }
}

// Complete task from next task card
async function completeTaskFromNext() {
    if (!currentNextTaskId) return;
    
    await completeTask(currentNextTaskId);
    document.getElementById('nextTaskCard').classList.add('hidden');
    currentNextTaskId = null;
}

// Load all tasks
async function loadTasks(sortByPriority = false) {
    try {
        if (isDemoMode()) {
            let filteredTasks = [...demoTasks];
            
            if (currentFilter === 'incomplete') {
                filteredTasks = demoTasks.filter(t => !t.completed);
            } else if (currentFilter === 'complete') {
                filteredTasks = demoTasks.filter(t => t.completed);
            }
            
            if (sortByPriority) {
                filteredTasks.sort((a, b) => b.priorityScore - a.priorityScore);
            }
            
            displayTasks(filteredTasks);
            return;
        }
        
        let url = `${API_URL}/tasks`;
        
        if (sortByPriority) {
            url = `${API_URL}/tasks/priority`;
        } else if (currentFilter === 'incomplete') {
            url = `${API_URL}/tasks?completed=false`;
        } else if (currentFilter === 'complete') {
            url = `${API_URL}/tasks?completed=true`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        displayTasks(data.tasks);
    } catch (error) {
        console.error('Error loading tasks:', error);
        document.getElementById('taskList').innerHTML = '<p class="loading">Failed to load tasks. Make sure the API is running.</p>';
    }
}

// Display tasks in the UI
function displayTasks(tasks) {
    const taskList = document.getElementById('taskList');
    
    if (!tasks || tasks.length === 0) {
        taskList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon"></div>
                <p>No tasks found. Click "New Task" to get started.</p>
            </div>
        `;
        return;
    }
    
    taskList.innerHTML = tasks.map(task => `
        <div class="task-item ${task.completed ? 'completed' : ''}" data-task-id="${task.id}">
            <div class="task-item-header">
                <div>
                    <div class="task-title">${escapeHtml(task.title)}</div>
                    ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
                </div>
                <div class="priority-badge">Score: ${task.priorityScore}</div>
            </div>
            
            <div class="task-meta">
                <span class="meta-item">Urgency: ${task.urgency}/10</span>
                <span class="meta-item">Importance: ${task.importance}/10</span>
                <span class="meta-item">Effort: ${task.estimatedEffort}/10</span>
                ${task.deadline ? `<span class="meta-item">Deadline: ${task.daysUntilDeadline} days (${new Date(task.deadline).toLocaleDateString()})</span>` : ''}
                ${task.isBlocked ? '<span class="meta-item">BLOCKED</span>' : ''}
            </div>
            
            <div class="task-actions">
                ${!task.completed ? `
                    <button class="btn btn-success btn-small" onclick="completeTask(${task.id})">
                        Complete
                    </button>
                ` : ''}
                <button class="btn btn-danger btn-small" onclick="deleteTask(${task.id})">
                    Delete
                </button>
            </div>
        </div>
    `).join('');
}

// Toggle add form visibility
function toggleAddForm() {
    const form = document.getElementById('addTaskForm');
    form.classList.toggle('hidden');
}

// Close AI card
function closeAiCard() {
    document.getElementById('nextTaskCard').classList.add('hidden');
    currentNextTaskId = null;
}

// Setup rating buttons
function setupRatingButtons() {
    const setupButtonGroup = (containerId) => {
        const container = document.getElementById(containerId);
        const buttons = container.querySelectorAll('.rating-btn');
        
        buttons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                // Remove active from all buttons in this group
                buttons.forEach(b => b.classList.remove('active'));
                // Add active to clicked button
                btn.classList.add('active');
            });
        });
    };
    
    setupButtonGroup('urgencyButtons');
    setupButtonGroup('importanceButtons');
    setupButtonGroup('effortButtons');
}

// Setup deadline buttons
function setupDeadlineButtons() {
    const deadlineButtons = document.querySelectorAll('.deadline-btn');
    const dateInput = document.getElementById('taskDeadline');
    
    deadlineButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active from all buttons
            deadlineButtons.forEach(b => b.classList.remove('active'));
            // Add active to clicked button
            btn.classList.add('active');
            
            const days = btn.getAttribute('data-days');
            
            if (days === 'custom') {
                dateInput.style.display = 'block';
                dateInput.focus();
            } else {
                dateInput.style.display = 'none';
                
                // Calculate date
                const date = new Date();
                date.setDate(date.getDate() + parseInt(days));
                
                // Format as YYYY-MM-DD
                const year = date.getFullYear();
                const month = String(date.getMonth() + 1).padStart(2, '0');
                const day = String(date.getDate()).padStart(2, '0');
                dateInput.value = `${year}-${month}-${day}`;
            }
        });
    });
}

// Setup form submission
function setupFormSubmit() {
    const form = document.getElementById('taskForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const title = document.getElementById('taskTitle').value;
        const description = document.getElementById('taskDescription').value;
        
        // Get selected rating values
        const urgency = parseInt(document.querySelector('#urgencyButtons .rating-btn.active').getAttribute('data-value'));
        const importance = parseInt(document.querySelector('#importanceButtons .rating-btn.active').getAttribute('data-value'));
        const estimatedEffort = parseInt(document.querySelector('#effortButtons .rating-btn.active').getAttribute('data-value'));
        
        const deadline = document.getElementById('taskDeadline').value || null;
        
        try {
            const response = await fetch(`${API_URL}/tasks`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    title,
                    description,
                    urgency,
                    importance,
                    estimatedEffort,
                    deadline,
                    dependencies: []
                })
            });
            
            if (response.ok) {
                form.reset();
                
                // Reset rating buttons to default (5)
                document.querySelectorAll('.rating-btn').forEach(btn => {
                    btn.classList.remove('active');
                    if (btn.getAttribute('data-value') === '5') {
                        btn.classList.add('active');
                    }
                });
                
                // Reset deadline buttons
                document.querySelectorAll('.deadline-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                document.getElementById('taskDeadline').style.display = 'none';
                document.getElementById('taskDeadline').value = '';
                
                // Hide form
                toggleAddForm();
                
                await loadTasks();
                await loadStats();
                
                // Show success message
                showNotification('Task added successfully', 'success');
            } else {
                const error = await response.json();
                alert(`Error: ${error.error}`);
            }
        } catch (error) {
            console.error('Error adding task:', error);
            alert('Failed to add task. Make sure the API is running.');
        }
    });
}

// Complete a task
async function completeTask(taskId) {
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}/complete`, {
            method: 'PATCH'
        });
        
        if (response.ok) {
            await loadTasks();
            await loadStats();
            showNotification('Task completed successfully', 'success');
        }
    } catch (error) {
        console.error('Error completing task:', error);
        alert('Failed to complete task.');
    }
}

// Delete a task
async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            await loadTasks();
            await loadStats();
            showNotification('Task deleted', 'success');
        }
    } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task.');
    }
}

// Filter tasks
function filterTasks(filter) {
    currentFilter = filter;
    
    // Update active button - find button by text content or filter type
    document.querySelectorAll('.filter-chip').forEach(btn => {
        btn.classList.remove('active');
        
        // Match button to filter
        const btnText = btn.textContent.trim().toLowerCase();
        if ((filter === 'all' && btnText === 'all tasks') ||
            (filter === 'incomplete' && btnText === 'active') ||
            (filter === 'complete' && btnText === 'completed')) {
            btn.classList.add('active');
        }
    });
    
    loadTasks();
}

// Sort by priority
function sortByPriority() {
    loadTasks(true);
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show notification
function showNotification(message, type = 'success') {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        font-weight: 600;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add slide animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

