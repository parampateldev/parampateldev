# 🎯 Task Priority API

An intelligent REST API that automatically prioritizes your tasks using a smart scoring algorithm. Unlike basic todo lists, this API considers multiple factors (urgency, importance, effort, deadline proximity, and dependencies) to tell you exactly what you should work on next.

## ✨ What Makes This Unique?

- **Intelligent Priority Scoring**: Automatically calculates priority scores based on multiple weighted factors
- **Smart Recommendations**: Suggests the next best task to work on
- **Dependency Tracking**: Tasks can depend on other tasks; blocked tasks get lower priority
- **Deadline Awareness**: Priority increases as deadlines approach
- **Effort Optimization**: Considers task effort in priority calculations
- **Productivity Analytics**: Track completion rates and performance metrics

## 🚀 Getting Started

### Installation

```bash
cd task-priority-api
npm install
```

### Run the Server

```bash
npm start
```

Or for development with auto-reload:

```bash
npm run dev
```

The API will be available at `http://localhost:3000`

## 📖 API Documentation

### Base URL
```
http://localhost:3000
```

### Endpoints

#### 1. Get API Info
```http
GET /
```

Returns API documentation and available endpoints.

---

#### 2. Get All Tasks
```http
GET /api/tasks
GET /api/tasks?completed=false
```

**Query Parameters:**
- `completed` (optional): `true` or `false` to filter by completion status

**Response:**
```json
{
  "count": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Finish project proposal",
      "description": "Complete the Q4 project proposal for client review",
      "urgency": 9,
      "importance": 10,
      "estimatedEffort": 3,
      "deadline": "2025-10-15",
      "dependencies": [],
      "completed": false,
      "createdAt": "2025-10-11T...",
      "priorityScore": 87.25,
      "daysUntilDeadline": 4,
      "isBlocked": false
    }
  ]
}
```

---

#### 3. Get Tasks Sorted by Priority
```http
GET /api/tasks/priority
```

Returns incomplete tasks sorted by priority score (highest first).

---

#### 4. Get Next Recommended Task
```http
GET /api/tasks/next
```

Returns the highest priority unblocked task you should work on next, plus alternatives.

**Response:**
```json
{
  "message": "This is your highest priority task",
  "task": {
    "id": 1,
    "title": "Finish project proposal",
    "priorityScore": 87.25,
    ...
  },
  "alternativeTasks": [...]
}
```

---

#### 5. Get Specific Task
```http
GET /api/tasks/:id
```

**Example:**
```http
GET /api/tasks/1
```

---

#### 6. Create New Task
```http
POST /api/tasks
Content-Type: application/json

{
  "title": "Review code",
  "description": "Review pull requests",
  "urgency": 7,
  "importance": 8,
  "estimatedEffort": 2,
  "deadline": "2025-10-13",
  "dependencies": []
}
```

**Required Fields:**
- `title` (string)

**Optional Fields:**
- `description` (string)
- `urgency` (number 1-10, default: 5) - How urgent is this?
- `importance` (number 1-10, default: 5) - How important is this?
- `estimatedEffort` (number 1-10, default: 5) - How much work is required?
- `deadline` (ISO date string, optional)
- `dependencies` (array of task IDs, default: [])

**Response:** Returns created task with priority score (201 Created)

---

#### 7. Update Task
```http
PUT /api/tasks/:id
Content-Type: application/json

{
  "title": "Updated title",
  "urgency": 9,
  "importance": 10
}
```

Updates any fields provided. Fields not included remain unchanged.

---

#### 8. Mark Task as Complete
```http
PATCH /api/tasks/:id/complete
```

Marks a task as completed and records completion timestamp.

---

#### 9. Delete Task
```http
DELETE /api/tasks/:id
```

Permanently deletes a task.

---

#### 10. Get Productivity Statistics
```http
GET /api/stats
```

**Response:**
```json
{
  "totalTasks": 10,
  "completedTasks": 6,
  "incompleteTasks": 4,
  "overdueTasks": 1,
  "highPriorityTasks": 2,
  "completionRate": 60,
  "averagePriorityScore": 65.5
}
```

---

## 🧮 Priority Score Algorithm

The priority score (0-100) is calculated using:

```
Priority = (Urgency × 0.30) + (Importance × 0.35) + (Effort × 0.15) + (Deadline × 0.20)
```

### Factors:

1. **Urgency (30% weight)**: How urgent is the task?
2. **Importance (35% weight)**: How important is it strategically?
3. **Effort (15% weight)**: Lower effort = higher priority (quick wins!)
4. **Deadline (20% weight)**: Closer deadlines = higher priority
   - Overdue: Maximum score
   - Due today: 95% score
   - Due tomorrow: 90% score
   - Due in 2-3 days: 70% score
   - Due this week: 40% score
   - Due later: 10% score

### Dependency Penalty:
Tasks with incomplete dependencies get their priority reduced by 70% (blocked tasks).

---

## 🎯 Example Usage

### Create a high-priority task
```bash
curl -X POST http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fix critical bug",
    "description": "Production bug affecting users",
    "urgency": 10,
    "importance": 10,
    "estimatedEffort": 2,
    "deadline": "2025-10-12"
  }'
```

### Get your next task
```bash
curl http://localhost:3000/api/tasks/next
```

### Mark task as complete
```bash
curl -X PATCH http://localhost:3000/api/tasks/1/complete
```

### Check your stats
```bash
curl http://localhost:3000/api/stats
```

---

## 🛠️ Use Cases

- **Personal Productivity**: Manage your daily tasks intelligently
- **Team Task Management**: API for building team productivity apps
- **Project Planning**: Track project tasks with dependencies
- **Time Management**: Optimize what to work on next
- **Deadline Tracking**: Never miss important deadlines
- **Analytics**: Track productivity trends over time

---

## 🔮 Future Enhancements

Potential features to add:
- [ ] User authentication & multi-user support
- [ ] Database persistence (PostgreSQL/MongoDB)
- [ ] Recurring tasks
- [ ] Task categories/tags
- [ ] Time tracking per task
- [ ] Machine learning to improve priority predictions based on your behavior
- [ ] Email/push notifications for high-priority tasks
- [ ] Integration with calendar apps
- [ ] Team collaboration features
- [ ] GraphQL endpoint

---

## 🏗️ Tech Stack

- **Node.js** - Runtime
- **Express.js** - Web framework
- **CORS** - Cross-origin support
- **Pure JavaScript** - No database required (uses in-memory storage)

---

## 📝 License

MIT License - Feel free to use this in your projects!

---

## 👨‍💻 Author

**Param Patel**

---

## 🤝 Contributing

Feel free to fork, improve, and submit pull requests!

---

**Happy prioritizing! 🎯**

