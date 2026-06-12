# OCSS - Developer Documentation

## Architecture Overview

OCSS follows a modular architecture with:
- **Frontend**: Streamlit pages
- **Business Logic**: Utility modules
- **Data Layer**: SQLite database
- **File Management**: Local filesystem for uploads

## Core Modules

### Database Module (`database/db_init.py`)

#### Functions

**`init_database()`**
- Initializes SQLite database with all required tables
- Called on first app startup
- Creates schema for semesters, subjects, exams, notes, tasks, etc.

**`get_connection()`**
- Returns SQLite database connection
- Usage: `conn = get_connection()`
- Remember to close: `conn.close()`

#### Database Tables

- **semesters**: id, name, start_date, end_date, created_at
- **subjects**: id, semester_id, name, folder_path, created_at
- **exams**: id, subject_id, name, exam_date, marks, created_at
- **uploads**: id, subject_id, filename, file_path, file_type, upload_date
- **notes**: id, subject_id, title, content, created_at, updated_at
- **planner_tasks**: id, subject_id, title, description, due_date, priority, completed, created_at
- **mock_tests**: id, subject_id, title, total_marks, obtained_marks, num_questions, difficulty, test_type, created_at
- **progress**: id, subject_id, hours_studied, completion_percentage, revision_status, updated_at
- **flashcards**: id, subject_id, question, answer, created_at

### File Manager Module (`utils/file_manager.py`)

#### Functions

**`create_subject_folder(subject_name, semester_name)`**
- Creates folder structure: `uploads/semester_name/subject_name/`
- Returns: folder path (string)

**`save_uploaded_file(uploaded_file, subject_folder)`**
- Saves Streamlit uploaded file to disk
- Parameters: 
  - uploaded_file: UploadedFile object from Streamlit
  - subject_folder: destination folder path
- Returns: file path (string)

**`is_allowed_file(filename)`**
- Validates file type against allowed extensions
- Allowed: .pdf, .pptx, .docx, .png, .jpg, .jpeg, .gif
- Returns: boolean

**`get_files_in_folder(folder_path)`**
- Lists all files in a folder
- Returns: List of dicts with 'name', 'path', 'size', 'type'

**`delete_file(file_path)`**
- Removes a file from disk
- Returns: boolean (True if successful)

**`get_file_size_mb(file_path)`**
- Gets file size in megabytes
- Returns: float

### Planner Module (`utils/planner.py`)

#### Functions

**`add_task(subject_id, title, description, due_date, priority='Medium')`**
- Creates a new planner task
- Priority: 'Low', 'Medium', 'High'
- Returns: task_id (integer)

**`get_tasks(subject_id=None)`**
- Retrieves tasks, optionally filtered by subject
- Returns: List of task tuples

**`mark_task_complete(task_id)`**
- Marks a task as completed
- Returns: None

**`update_task(task_id, title, description, due_date, priority)`**
- Updates existing task
- Returns: None

**`delete_task(task_id)`**
- Removes a task
- Returns: None

**`get_upcoming_tasks(days=7)`**
- Gets tasks due within N days
- Returns: List of task tuples

**`generate_revision_schedule(exam_date, subject_id, num_sessions=10)`**
- Creates automatic revision tasks for an exam
- Parameters:
  - exam_date: date string (YYYY-MM-DD)
  - subject_id: integer
  - num_sessions: number of revision sessions (5-20)
- Returns: List of schedule dicts

### Quiz Generator Module (`utils/quiz_generator.py`)

#### Functions

**`create_mock_test(subject_id, title, total_marks, num_questions, difficulty, test_type)`**
- Creates a new mock test
- difficulty: 'Easy', 'Medium', 'Hard'
- test_type: 'MCQ', 'Short Answer', 'Long Answer', 'Mixed'
- Returns: test_id (integer)

**`get_mock_tests(subject_id=None)`**
- Retrieves tests, optionally filtered by subject
- Returns: List of test tuples

**`update_test_score(test_id, obtained_marks)`**
- Updates test score after completion
- Returns: None

**`generate_sample_questions(num_questions, difficulty, test_type)`**
- Generates sample questions based on parameters
- Returns: List of question dicts with 'number', 'question', 'options', 'answer'

**`calculate_test_performance(total_marks, obtained_marks)`**
- Calculates percentage, grade (A-D), etc.
- Returns: Dict with 'percentage', 'grade', 'obtained', 'total'

**`get_test_statistics(subject_id)`**
- Gets overall test stats for a subject
- Returns: Dict with 'total_tests', 'avg_percentage', 'best_percentage', 'worst_percentage'

### Analytics Module (`utils/analytics.py`)

#### Functions

**`update_study_hours(subject_id, hours)`**
- Adds to total study hours for a subject
- Returns: None

**`update_completion_percentage(subject_id, percentage)`**
- Updates subject completion percentage (0-100)
- Returns: None

**`update_revision_status(subject_id, status)`**
- Updates revision status ('Not Started', 'In Progress', 'Completed')
- Returns: None

**`get_progress(subject_id)`**
- Retrieves progress data for a subject
- Returns: Dict with 'hours_studied', 'completion_percentage', 'revision_status'

**`get_dashboard_stats()`**
- Gets overall dashboard statistics
- Returns: Dict with 'total_hours', 'avg_completion', 'num_subjects', 'recent_activity'

**`calculate_weekly_streak()`**
- Calculates study streak (days studied in last 7 days)
- Returns: integer (0-7)

**`get_upcoming_deadlines()`**
- Gets upcoming exam deadlines
- Returns: List of exam tuples

**`get_weak_topics(subject_id)`**
- Identifies weak topics based on test performance
- Returns: List of dicts with 'topic', 'score', 'status'

## Page Modules

### Dashboard (`pages/Dashboard.py`)

Displays overall statistics and progress.

**Key Metrics:**
- Total hours studied
- Average completion percentage
- Active subjects
- Weekly streak

**Visualizations:**
- Subject completion bar chart
- Study time pie chart

### Subjects (`pages/Subjects.py`)

Manages subjects and semesters.

**Tabs:**
1. **View Subjects**: Lists all subjects with stats
2. **Add Subject**: Creates new subject
3. **Manage**: Updates hours and completion

### Notes (`pages/Notes.py`)

Rich-text note management with search.

**Tabs:**
1. **View Notes**: Lists notes by subject
2. **Create Note**: Creates new note
3. **Search**: Searches across all notes

### Planner (`pages/Planner.py`)

Study planning and task management.

**Tabs:**
1. **Calendar View**: Shows all events
2. **Add Task**: Creates new task
3. **Upcoming**: Shows tasks for next 7 days
4. **Revision Schedule**: Auto-generates revision tasks

### Mock Tests (`pages/Mock_Tests.py`)

Test creation and performance tracking.

**Tabs:**
1. **Create Test**: Creates new test
2. **My Tests**: Lists all tests
3. **Statistics**: Performance analytics

### Progress (`pages/Progress.py`)

Detailed progress tracking and analytics.

**Sections:**
- Overall statistics
- Subject-wise progress
- Revision timeline
- Mock test performance
- Weak topics analysis

### AI Assistant (`pages/AI_Assistant.py`)

AI-powered study features.

**Tabs:**
1. **Summarize**: Document summarization
2. **Q&A**: Question answering
3. **Flashcards**: Auto-generated flashcards
4. **Concept Explanation**: Detailed explanations
5. **Revision Notes**: Condensed notes

## Usage Examples

### Creating a Semester with Subjects

```python
from database.db_init import get_connection
from utils.file_manager import create_subject_folder
from utils.planner import generate_revision_schedule

conn = get_connection()
cursor = conn.cursor()

# Create semester
cursor.execute('''
    INSERT INTO semesters (name, start_date, end_date)
    VALUES (?, ?, ?)
''', ('Fall 2024', '2024-09-01', '2024-12-15'))

semester_id = cursor.lastrowid

# Create subject
subject_folder = create_subject_folder('Physics', 'Fall 2024')
cursor.execute('''
    INSERT INTO subjects (semester_id, name, folder_path)
    VALUES (?, ?, ?)
''', (semester_id, 'Physics', subject_folder))

subject_id = cursor.lastrowid
conn.commit()
conn.close()
```

### Adding Study Hours and Updating Progress

```python
from utils.analytics import update_study_hours, update_completion_percentage

subject_id = 1
update_study_hours(subject_id, 2.5)  # Add 2.5 hours
update_completion_percentage(subject_id, 75)  # Set to 75% complete
```

### Creating and Scoring a Mock Test

```python
from utils.quiz_generator import create_mock_test, update_test_score

subject_id = 1
test_id = create_mock_test(
    subject_id=subject_id,
    title="Physics Chapter 1 Test",
    total_marks=100,
    num_questions=20,
    difficulty="Medium",
    test_type="MCQ"
)

# After test completion
update_test_score(test_id, 85)  # User scored 85 marks
```

## Best Practices

1. **Always close database connections**: Use `try-finally` or context managers
2. **Validate user inputs**: Check file types, date formats, numeric ranges
3. **Use transactions**: Wrap related operations in `conn.commit()`
4. **Handle exceptions**: Catch and log database errors gracefully
5. **Cache expensive operations**: Avoid repeated database queries
6. **Clean up temp files**: Delete uploaded files after processing
7. **Optimize queries**: Use indexes on frequently searched columns
8. **Document changes**: Update docstrings when modifying functions

## Performance Considerations

- **Database**: SQLite suitable for single-user scenarios; consider PostgreSQL for multi-user
- **File uploads**: Implement file size limits (max 100MB recommended)
- **Search**: Add database indexes on frequently searched columns
- **Caching**: Use Streamlit's @st.cache_data for expensive computations
- **UI**: Lazy-load large datasets with pagination

## Future Enhancements

- [ ] Implement user authentication
- [ ] Add database migrations framework (Alembic)
- [ ] Integrate real AI API (OpenAI, Claude)
- [ ] Add cloud storage integration (S3, Google Drive)
- [ ] Implement real-time collaboration
- [ ] Add mobile API (REST/GraphQL)
- [ ] Implement caching layer (Redis)
- [ ] Add async task processing (Celery)
