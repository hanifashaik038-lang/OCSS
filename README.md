# 📚 OCSS - Online Collaborative Study System

A comprehensive web-based study management platform built with Streamlit that helps students organize their studies, manage notes, plan revisions, and track progress across multiple subjects.

## ✨ Features

### 📖 Core Features

- **📅 Semester Setup**: One-click semester creation with automatic subject and exam setup
- **📚 Subject Management**: Organize subjects by semester with progress tracking
- **📝 Rich Notes Editor**: Create, edit, and search notes with auto-save functionality
- **📤 File Management**: Upload and organize PDFs, presentations, documents, and images
- **📅 Study Planner**: Calendar view, daily schedules, task management, and Pomodoro timer
- **✅ Mock Tests**: Generate practice tests and track performance
- **📊 Progress Dashboard**: Real-time analytics on study hours, completion, and performance
- **🤖 AI Assistant**: Summarize documents, answer questions, generate flashcards

### 🎯 Advanced Features

- **Exam Countdown**: Track days until exams and auto-generate revision schedules
- **Weak Topic Identification**: Analyze test performance to identify areas needing focus
- **Universal Search**: Search across notes, PDFs, flashcards, and summaries
- **Offline Support**: Access notes, files, and flashcards without internet
- **Weekly Streak Tracking**: Gamification with study streak statistics

## 🗂️ Project Structure

```
OCSS/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── database/
│   └── db_init.py        # Database initialization and schema
├── pages/
│   ├── Dashboard.py      # Dashboard with statistics
│   ├── Subjects.py       # Subject management
│   ├── Notes.py          # Note-taking module
│   ├── Planner.py        # Study planner
│   ├── Mock_Tests.py     # Mock test generator
│   ├── Progress.py       # Progress analytics
│   └── AI_Assistant.py   # AI-powered study features
├── utils/
│   ├── file_manager.py   # File upload and management
│   ├── planner.py        # Planner utilities
│   ├── quiz_generator.py # Mock test generation
│   └── analytics.py      # Progress tracking and analytics
├── uploads/              # User uploaded files
├── data/                 # Temporary data storage
└── assets/               # Images and static files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or extract the project folder)
   ```bash
   cd OCSS
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python database/db_init.py
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### Step 1: Create a Semester Setup
1. Go to **⚙️ Setup** in the sidebar
2. Enter semester details (name, start/end dates)
3. Add subjects and their exam dates
4. Click "Create Semester Setup"
5. The system will automatically:
   - Create subject folders
   - Initialize progress tracking
   - Generate revision schedules

### Step 2: Upload Study Materials
1. Go to **📤 Uploads**
2. Select a subject
3. Upload PDFs, presentations, documents, or images
4. Files are automatically organized by subject

### Step 3: Create and Manage Notes
1. Go to **📝 Notes**
2. Click "Create Note"
3. Select subject and write your notes
4. Notes auto-save every change
5. Use search to find notes across all subjects

### Step 4: Plan Your Studies
1. Go to **📅 Planner**
2. View calendar with all tasks and exams
3. Add new tasks with priorities
4. Generate automatic revision schedules for exams
5. Mark tasks as complete to track progress

### Step 5: Create Mock Tests
1. Go to **✅ Mock Tests**
2. Click "Create Test"
3. Select difficulty, number of questions, and test type (MCQ, Short Answer, etc.)
4. Complete the test
5. View performance analytics

### Step 6: Track Progress
1. Go to **📊 Progress**
2. View overall statistics:
   - Total hours studied
   - Subject completion percentage
   - Weekly study streak
   - Mock test performance
3. Identify weak topics based on test scores

### Step 7: Use AI Assistant
1. Go to **🤖 AI Assistant**
2. Available features:
   - **Summarize**: Get AI-generated document summaries
   - **Q&A**: Ask questions about your materials
   - **Flashcards**: Auto-generate flashcards for topics
   - **Concept Explanation**: Get detailed explanations
   - **Revision Notes**: Create condensed revision notes

## 🗄️ Database Schema

### Tables

- **semesters**: Stores semester information
- **subjects**: Subject details with folder paths
- **exams**: Exam information and dates
- **uploads**: Uploaded files metadata
- **notes**: User notes with timestamps
- **planner_tasks**: Tasks and assignments
- **mock_tests**: Test information and scores
- **progress**: Study hours and completion tracking
- **flashcards**: Flashcard data for revision

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python
- **Database**: SQLite
- **Visualization**: Plotly
- **File Handling**: python-pptx, python-docx, PyPDF2
- **UI Components**: Streamlit widgets

## 📋 Requirements

All requirements are listed in `requirements.txt`:
- streamlit
- pandas
- plotly
- python-pptx
- python-docx
- PyPDF2
- pillow
- openai (for AI features)
- requests

## 🔧 Configuration

### Streamlit Config
Edit `.streamlit/config.toml` to customize:
- Theme colors
- Font settings
- Server configuration
- Logging levels

### Environment Variables
Create a `.env` file for sensitive data:
```
OPENAI_API_KEY=your_api_key_here
```

## 💾 Data Storage

- **Database**: `database/app.db` (SQLite)
- **User Uploads**: `uploads/` (organized by semester/subject)
- **Temporary Data**: `data/` folder
- **Assets**: `assets/` folder for images

## 🔐 Security Notes

- Store API keys in `.env` file (not in code)
- Database is local and not exposed
- File uploads are restricted to safe file types
- All user data remains on local machine

## 🧪 Testing

### Manual Testing Checklist (Step 17)

- [ ] Folder creation for semesters and subjects
- [ ] File upload functionality (PDF, PPT, DOCX, Images)
- [ ] Planner task creation and completion
- [ ] Notes creation, editing, and searching
- [ ] Mock test generation and scoring
- [ ] Progress dashboard calculations
- [ ] Database persistence across sessions
- [ ] AI features (summarization, Q&A, etc.)

## 🚦 Future Enhancements

- [ ] Collaborative features for group study
- [ ] Mobile app version
- [ ] Advanced AI integration with OpenAI API
- [ ] Real-time synchronization with cloud storage
- [ ] Integration with calendar apps (Google Calendar, Outlook)
- [ ] Video recording and playback of notes
- [ ] Peer-to-peer study matching
- [ ] Advanced analytics and ML predictions

## 📝 Contributing

To contribute to this project:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Support

For issues, questions, or suggestions:
- Open an issue on the repository
- Check existing documentation
- Review the troubleshooting section

## 📞 Contact

For questions or feedback about OCSS, please reach out to the development team.

---

**Happy Studying! 📚✨**

*Last Updated: 2026*
