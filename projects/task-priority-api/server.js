const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// In-memory database (in production, use a real database)
let tasks = [
  {
    id: 1,
    title: "Finish project proposal",
    description: "Complete the Q4 project proposal for client review",
    urgency: 9,
    importance: 10,
    estimatedEffort: 3,
    deadline: "2025-10-15",
    dependencies: [],
    completed: false,
    createdAt: new Date().toISOString()
  },
  {
    id: 2,
    title: "Review code PRs",
    description: "Review 3 pending pull requests",
    urgency: 7,
    importance: 6,
    estimatedEffort: 1,
    deadline: "2025-10-12",
    dependencies: [],
    completed: false,
    createdAt: new Date().toISOString()
  }
];

let nextId = 3;

// ==================== HELPER FUNCTIONS ====================

/**
 * Calculate intelligent priority score for a task
 * Score is based on: urgency, importance, effort, deadline proximity, dependencies
 */
function calculatePriorityScore(task) {
  const urgencyWeight = 0.3;
  const importanceWeight = 0.35;
  const effortWeight = 0.15; // Lower effort = higher priority
  const deadlineWeight = 0.2;
  
  // Normalize urgency and importance (1-10 scale)
  const urgencyScore = (task.urgency / 10) * urgencyWeight;
  const importanceScore = (task.importance / 10) * importanceWeight;
  
  // Effort score - lower effort gets higher score (inverted)
  const effortScore = ((10 - task.estimatedEffort) / 10) * effortWeight;
  
  // Deadline proximity score
  let deadlineScore = 0;
  if (task.deadline) {
    const daysUntilDeadline = Math.ceil(
      (new Date(task.deadline) - new Date()) / (1000 * 60 * 60 * 24)
    );
    
    if (daysUntilDeadline < 0) {
      deadlineScore = 1; // Overdue - max score
    } else if (daysUntilDeadline === 0) {
      deadlineScore = 0.95; // Due today
    } else if (daysUntilDeadline <= 1) {
      deadlineScore = 0.9; // Due tomorrow
    } else if (daysUntilDeadline <= 3) {
      deadlineScore = 0.7; // Due in 2-3 days
    } else if (daysUntilDeadline <= 7) {
      deadlineScore = 0.4; // Due this week
    } else {
      deadlineScore = 0.1; // Due later
    }
  }
  deadlineScore *= deadlineWeight;
  
  // Check if blocked by dependencies
  const hasUncompletedDependencies = task.dependencies.some(depId => {
    const depTask = tasks.find(t => t.id === depId);
    return depTask && !depTask.completed;
  });
  
  // If blocked, reduce priority significantly
  const dependencyPenalty = hasUncompletedDependencies ? 0.3 : 1;
  
  // Calculate total score (0-100)
  const totalScore = (urgencyScore + importanceScore + effortScore + deadlineScore) * 100 * dependencyPenalty;
  
  return Math.round(totalScore * 100) / 100; // Round to 2 decimal places
}

/**
 * Add computed fields to task
 */
function enrichTask(task) {
  return {
    ...task,
    priorityScore: calculatePriorityScore(task),
    daysUntilDeadline: task.deadline 
      ? Math.ceil((new Date(task.deadline) - new Date()) / (1000 * 60 * 60 * 24))
      : null,
    isBlocked: task.dependencies.some(depId => {
      const depTask = tasks.find(t => t.id === depId);
      return depTask && !depTask.completed;
    })
  };
}

// ==================== API ROUTES ====================

/**
 * GET / - API Info
 */
app.get('/', (req, res) => {
  res.json({
    name: "Task Priority API",
    version: "1.0.0",
    description: "Intelligent task prioritization with AI-powered scoring",
    endpoints: {
      "GET /api/tasks": "Get all tasks with priority scores",
      "GET /api/tasks/priority": "Get tasks sorted by priority (highest first)",
      "GET /api/tasks/next": "Get the next recommended task to work on",
      "GET /api/tasks/:id": "Get a specific task",
      "POST /api/tasks": "Create a new task",
      "PUT /api/tasks/:id": "Update a task",
      "PATCH /api/tasks/:id/complete": "Mark task as completed",
      "DELETE /api/tasks/:id": "Delete a task",
      "GET /api/stats": "Get productivity statistics"
    }
  });
});

/**
 * GET /api/tasks - Get all tasks
 */
app.get('/api/tasks', (req, res) => {
  const { completed } = req.query;
  
  let filteredTasks = tasks;
  
  // Filter by completion status if specified
  if (completed !== undefined) {
    const isCompleted = completed === 'true';
    filteredTasks = tasks.filter(t => t.completed === isCompleted);
  }
  
  const enrichedTasks = filteredTasks.map(enrichTask);
  res.json({
    count: enrichedTasks.length,
    tasks: enrichedTasks
  });
});

/**
 * GET /api/tasks/priority - Get tasks sorted by priority
 */
app.get('/api/tasks/priority', (req, res) => {
  const incompleteTasks = tasks
    .filter(t => !t.completed)
    .map(enrichTask)
    .sort((a, b) => b.priorityScore - a.priorityScore);
  
  res.json({
    count: incompleteTasks.length,
    tasks: incompleteTasks
  });
});

/**
 * GET /api/tasks/next - Get the next recommended task
 */
app.get('/api/tasks/next', (req, res) => {
  const incompleteTasks = tasks
    .filter(t => !t.completed)
    .map(enrichTask)
    .filter(t => !t.isBlocked) // Only unblocked tasks
    .sort((a, b) => b.priorityScore - a.priorityScore);
  
  if (incompleteTasks.length === 0) {
    return res.json({
      message: "No tasks available. Great job!",
      task: null
    });
  }
  
  res.json({
    message: "This is your highest priority task",
    task: incompleteTasks[0],
    alternativeTasks: incompleteTasks.slice(1, 4) // Show top 3 alternatives
  });
});

/**
 * GET /api/tasks/:id - Get a specific task
 */
app.get('/api/tasks/:id', (req, res) => {
  const task = tasks.find(t => t.id === parseInt(req.params.id));
  
  if (!task) {
    return res.status(404).json({ error: 'Task not found' });
  }
  
  res.json(enrichTask(task));
});

/**
 * POST /api/tasks - Create a new task
 */
app.post('/api/tasks', (req, res) => {
  const { title, description, urgency, importance, estimatedEffort, deadline, dependencies } = req.body;
  
  // Validation
  if (!title) {
    return res.status(400).json({ error: 'Title is required' });
  }
  
  if (urgency && (urgency < 1 || urgency > 10)) {
    return res.status(400).json({ error: 'Urgency must be between 1 and 10' });
  }
  
  if (importance && (importance < 1 || importance > 10)) {
    return res.status(400).json({ error: 'Importance must be between 1 and 10' });
  }
  
  if (estimatedEffort && (estimatedEffort < 1 || estimatedEffort > 10)) {
    return res.status(400).json({ error: 'Estimated effort must be between 1 and 10' });
  }
  
  const newTask = {
    id: nextId++,
    title,
    description: description || '',
    urgency: urgency || 5,
    importance: importance || 5,
    estimatedEffort: estimatedEffort || 5,
    deadline: deadline || null,
    dependencies: dependencies || [],
    completed: false,
    createdAt: new Date().toISOString()
  };
  
  tasks.push(newTask);
  res.status(201).json(enrichTask(newTask));
});

/**
 * PUT /api/tasks/:id - Update a task
 */
app.put('/api/tasks/:id', (req, res) => {
  const taskIndex = tasks.findIndex(t => t.id === parseInt(req.params.id));
  
  if (taskIndex === -1) {
    return res.status(404).json({ error: 'Task not found' });
  }
  
  const { title, description, urgency, importance, estimatedEffort, deadline, dependencies, completed } = req.body;
  
  // Validation
  if (urgency && (urgency < 1 || urgency > 10)) {
    return res.status(400).json({ error: 'Urgency must be between 1 and 10' });
  }
  
  if (importance && (importance < 1 || importance > 10)) {
    return res.status(400).json({ error: 'Importance must be between 1 and 10' });
  }
  
  if (estimatedEffort && (estimatedEffort < 1 || estimatedEffort > 10)) {
    return res.status(400).json({ error: 'Estimated effort must be between 1 and 10' });
  }
  
  const updatedTask = {
    ...tasks[taskIndex],
    title: title !== undefined ? title : tasks[taskIndex].title,
    description: description !== undefined ? description : tasks[taskIndex].description,
    urgency: urgency !== undefined ? urgency : tasks[taskIndex].urgency,
    importance: importance !== undefined ? importance : tasks[taskIndex].importance,
    estimatedEffort: estimatedEffort !== undefined ? estimatedEffort : tasks[taskIndex].estimatedEffort,
    deadline: deadline !== undefined ? deadline : tasks[taskIndex].deadline,
    dependencies: dependencies !== undefined ? dependencies : tasks[taskIndex].dependencies,
    completed: completed !== undefined ? completed : tasks[taskIndex].completed,
    updatedAt: new Date().toISOString()
  };
  
  tasks[taskIndex] = updatedTask;
  res.json(enrichTask(updatedTask));
});

/**
 * PATCH /api/tasks/:id/complete - Mark task as completed
 */
app.patch('/api/tasks/:id/complete', (req, res) => {
  const taskIndex = tasks.findIndex(t => t.id === parseInt(req.params.id));
  
  if (taskIndex === -1) {
    return res.status(404).json({ error: 'Task not found' });
  }
  
  tasks[taskIndex].completed = true;
  tasks[taskIndex].completedAt = new Date().toISOString();
  
  res.json({
    message: 'Task marked as completed!',
    task: enrichTask(tasks[taskIndex])
  });
});

/**
 * DELETE /api/tasks/:id - Delete a task
 */
app.delete('/api/tasks/:id', (req, res) => {
  const taskIndex = tasks.findIndex(t => t.id === parseInt(req.params.id));
  
  if (taskIndex === -1) {
    return res.status(404).json({ error: 'Task not found' });
  }
  
  const deletedTask = tasks[taskIndex];
  tasks.splice(taskIndex, 1);
  
  res.json({
    message: 'Task deleted successfully',
    task: deletedTask
  });
});

/**
 * GET /api/stats - Get productivity statistics
 */
app.get('/api/stats', (req, res) => {
  const completedTasks = tasks.filter(t => t.completed);
  const incompleteTasks = tasks.filter(t => !t.completed);
  const overdueTasks = incompleteTasks.filter(t => {
    if (!t.deadline) return false;
    return new Date(t.deadline) < new Date();
  });
  
  const avgPriorityScore = incompleteTasks.length > 0
    ? incompleteTasks.reduce((sum, t) => sum + calculatePriorityScore(t), 0) / incompleteTasks.length
    : 0;
  
  const highPriorityTasks = incompleteTasks.filter(t => calculatePriorityScore(t) > 70);
  
  res.json({
    totalTasks: tasks.length,
    completedTasks: completedTasks.length,
    incompleteTasks: incompleteTasks.length,
    overdueTasks: overdueTasks.length,
    highPriorityTasks: highPriorityTasks.length,
    completionRate: tasks.length > 0 
      ? Math.round((completedTasks.length / tasks.length) * 100) 
      : 0,
    averagePriorityScore: Math.round(avgPriorityScore * 100) / 100
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Task Priority API running on http://localhost:${PORT}`);
  console.log(`📚 Visit http://localhost:${PORT} for API documentation`);
});

