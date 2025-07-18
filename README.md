# Time-Aware Task Management System

A Django-based task management application with automatic time-aware status updates and modern web interface.

## Features

### Backend Features
- **REST API**: Robust, scalable, and secure API built with Django REST Framework
- **Time-Aware Auto-Bucketing**: Automatically categorizes tasks based on deadlines:
  - **Upcoming**: Tasks with future deadlines that are not completed
  - **Completed**: Tasks manually marked as complete
  - **Missed**: Tasks with past deadlines that were not completed
- **Manual Task Management**: Create, read, update, and delete tasks
- **Automatic Status Updates**: Tasks automatically transition between states based on time
- **Urgency Levels**: Tasks are classified as high, medium, or low urgency based on deadline proximity
- **Robust Validation**: Prevents invalid data entry and maintains data integrity

### 🤖 AI-Powered Features
- **Natural Language Task Creation**: Create tasks by describing them in plain English
- **Intelligent Task Breakdown**: Automatically break complex tasks into actionable subtasks
- **Smart Task Enhancement**: AI-powered suggestions to improve task descriptions
- **Productivity Insights**: AI analyzes your task patterns and provides actionable recommendations
- **Conflict Detection**: Automatically detects scheduling conflicts and suggests resolutions
- **Smart Reminders**: Personalized, motivational reminders based on task context and urgency
- **Priority Recommendations**: AI suggests optimal task priorities based on deadlines and importance
- **Time Estimation**: Intelligent estimates of task duration based on complexity

### Frontend Features
- **Modern UI**: Clean, minimal, and responsive design
- **Task Buckets**: Visual separation of tasks by status using cards/columns
- **Real-time Updates**: Automatic refresh every 30 seconds
- **Instant Feedback**: Visual feedback when task states change
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- **Statistics Dashboard**: Overview of task counts and urgency levels

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd task_manager
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv task_manager
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API Key** (for AI features):
   ```bash
    nano .env
   ```
   add the api key there

5. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

**Quick Setup**: Double-click `setup_and_run.bat` for automated setup with AI configuration.

## API Endpoints

### Tasks
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `POST /api/tasks/{id}/mark_completed/` - Mark task as completed
- `POST /api/tasks/{id}/mark_incomplete/` - Mark task as incomplete

### Special Endpoints
- `GET /api/tasks/buckets/` - Get tasks organized by status buckets
- `GET /api/tasks/stats/` - Get task statistics

### 🤖 AI-Powered Endpoints
- `POST /api/tasks/ai_create/` - Create task from natural language
- `POST /api/tasks/{id}/ai_breakdown/` - Break down task into subtasks
- `POST /api/tasks/{id}/ai_enhance/` - Enhance task description
- `GET /api/tasks/ai_insights/` - Get productivity insights
- `GET /api/tasks/ai_conflicts/` - Detect task conflicts
- `GET /api/tasks/{id}/ai_reminder/` - Generate smart reminder

### Query Parameters
- `status` - Filter by task status (upcoming, completed, missed)
- `urgency` - Filter by urgency level (high, medium, low)

## Time-Aware Features

### Automatic Status Updates
Tasks automatically transition between three states:
- **Upcoming**: Default state for tasks with future deadlines
- **Completed**: Set when user manually marks task as complete
- **Missed**: Automatically set when deadline passes without completion

### Urgency Classification
Tasks are automatically classified based on time until deadline:
- **High**: 1 day or less until deadline
- **Medium**: 2-3 days until deadline
- **Low**: More than 3 days until deadline

### Auto-Bucketing
The system automatically categorizes tasks into buckets for easy management:
- Updates happen in real-time when accessing the API
- Management command available for batch updates
- Frontend automatically refreshes to show current state

## Management Commands

Update all task statuses based on current time:
```bash
python manage.py update_task_status --verbose
```

## Project Structure

```
task_manager/
├── manage.py
├── requirements.txt
├── .env
├── task_manager_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializer.py
│   ├── urls.py
│   ├── views.py
│   └── management/
│       └── update_task_status.py
└── templates/
    └── home.html

```

## SOLID Principles Implementation

1. **Single Responsibility Principle**: Each class has a single, well-defined responsibility
2. **Open/Closed Principle**: Code is open for extension but closed for modification
3. **Liskov Substitution Principle**: Derived classes are substitutable for base classes
4. **Interface Segregation Principle**: Interfaces are focused and specific
5. **Dependency Inversion Principle**: High-level modules don't depend on low-level modules

## Technology Stack

- **Backend**: Django 5.2.4, Django REST Framework
- **Database**: SQLite (development), easily configurable for PostgreSQL/MySQL
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: Modern CSS Grid/Flexbox with responsive design
- **Time Handling**: Django's timezone-aware datetime handling


### Code Style
The project follows PEP 8 style guidelines and Django best practices.

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Enhancements

- User authentication and authorization
- Task categories and tags
- Email notifications for approaching deadlines
- Task sharing and collaboration
- Advanced filtering and search
- Mobile app (React Native/Flutter)
- Push notifications
- Task templates
- Recurring tasks
- Time tracking
- Reports and analytics