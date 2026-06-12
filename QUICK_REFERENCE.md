# OCSS - Quick Reference Card

## 🚀 Quick Start

```bash
# Navigate to project
cd OCSS

# Create environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database/db_init.py

# Run application
streamlit run app.py
```

**Access**: http://localhost:8501

---

## 📋 Features at a Glance

| Feature | Location | What It Does |
|---------|----------|-------------|
| 📅 Semester Setup | ⚙️ Setup | Create semester with subjects & exams |
| 📚 Manage Subjects | 📖 Subjects | Add subjects, track hours, update progress |
| 📝 Notes | 📝 Notes | Create, edit, search notes by subject |
| 📤 Upload Files | 📤 Uploads | Upload PDF, PPT, DOCX, images |
| 📅 Planner | 📅 Planner | Create tasks, view calendar, generate revision plan |
| ✅ Mock Tests | ✅ Mock Tests | Generate tests, track scores, view analytics |
| 📊 Dashboard | 📊 Progress | View stats, analyze performance, identify weak areas |
| 🤖 AI Features | 🤖 AI Assistant | Summarize, Q&A, flashcards, explanations |

---

## 🗄️ Database Tables

```
semesters       → Store semesters
subjects        → Store subjects with folder paths
exams           → Store exam dates and marks
uploads         → Track uploaded files
notes           → Store note content
planner_tasks   → Store tasks and assignments
mock_tests      → Store test scores
progress        → Track study hours and completion
flashcards      → Store flashcards
```

---

## 📁 Project Structure

```
OCSS/
├── app.py              # Main app (900+ lines)
├── pages/              # 7 feature modules
│   ├── Dashboard.py
│   ├── Subjects.py
│   ├── Notes.py
│   ├── Planner.py
│   ├── Mock_Tests.py
│   ├── Progress.py
│   └── AI_Assistant.py
├── utils/              # 4 utility modules
│   ├── file_manager.py
│   ├── planner.py
│   ├── quiz_generator.py
│   └── analytics.py
├── database/           # Database setup
│   └── db_init.py
└── documentation files
    ├── README.md
    ├── SETUP_GUIDE.md
    ├── DEVELOPER_GUIDE.md
    └── DEPLOYMENT.md
```

---

## 🔧 Common Commands

### View Database
```bash
# Open database
sqlite3 database/app.db

# View tables
.tables

# Query data
SELECT * FROM subjects;
```

### Troubleshooting
```bash
# Reset database
rm database/app.db
python database/db_init.py

# Clear cache
rm -rf .streamlit/cache

# Change port
streamlit run app.py --server.port 8502
```

---

## 🎯 Typical Workflow

### First Time Setup
1. Go to **⚙️ Setup**
2. Enter semester name and dates
3. Add subjects with exam dates
4. Click "Create Semester Setup"
5. ✅ Folders and tasks auto-created!

### Daily Usage
1. **Upload** files: 📤 Uploads
2. **Take notes**: 📝 Notes
3. **Add tasks**: 📅 Planner
4. **Log hours**: 📖 Subjects → Manage
5. **Check progress**: 📊 Progress

### Exam Preparation
1. Create mock tests: ✅ Mock Tests
2. Review weak topics: 📊 Progress
3. Revise from notes: 📝 Notes
4. Use AI features: 🤖 AI Assistant

---

## 💾 Data Storage

- **Database**: `database/app.db` (SQLite)
- **Uploads**: `uploads/Semester/Subject/` (organized folders)
- **Configuration**: `.streamlit/config.toml`
- **Logs**: Streamlit logs in browser

---

## 📊 Key Metrics Tracked

- ⏱️ Hours studied per subject
- 📈 Subject completion percentage
- 🔥 Weekly study streak (0-7 days)
- 📝 Total notes created
- 📤 Files uploaded
- ✅ Tests completed
- 🎯 Test scores and grades
- 📊 Weak topics identified

---

## 🔐 Security Notes

- Store API keys in `.env` (never commit!)
- Database is local (your data stays local)
- No internet required for core features
- File uploads limited to safe types
- All data is yours

---

## 📚 Documentation

| Document | For | Contains |
|----------|-----|----------|
| README.md | Everyone | Features, overview, usage |
| SETUP_GUIDE.md | Installation | Step-by-step setup, troubleshooting |
| DEVELOPER_GUIDE.md | Developers | API docs, code examples |
| DEPLOYMENT.md | Deployment | How to deploy (AWS, Heroku, Docker, etc.) |
| IMPLEMENTATION_SUMMARY.md | Reference | Complete implementation details |

---

## 🚀 Deployment Options

| Platform | Setup | Cost |
|----------|-------|------|
| **Local** | `streamlit run app.py` | Free |
| **Streamlit Cloud** | Push to GitHub, deploy | Free (with limits) |
| **Docker** | `docker build -t ocss . && docker run` | Your servers |
| **Heroku** | `git push heroku main` | $5-50/month |
| **AWS** | EC2 or Elastic Beanstalk | Pay-as-you-go |
| **Google Cloud** | Cloud Run | Free tier + usage |

---

## 🔄 Backup & Recovery

```bash
# Backup
cp database/app.db database/app.db.backup
cp -r uploads/ uploads.backup/

# Restore
cp database/app.db.backup database/app.db
cp -r uploads.backup/ uploads/
```

---

## ✅ Testing Checklist

- [ ] Create semester with 3 subjects
- [ ] Upload 2-3 files for each subject
- [ ] Create 5 notes in different subjects
- [ ] Add 10 tasks to planner
- [ ] Generate mock test (10 questions)
- [ ] Search for notes
- [ ] Check progress dashboard
- [ ] Log study hours
- [ ] Refresh page and verify data persists

---

## 💡 Tips & Tricks

1. **Quick Semester Setup**: Enter all data at once in setup wizard
2. **Organize Files**: Use subject folders to auto-organize
3. **Revision Planning**: Let system auto-generate revision schedule
4. **Weak Topics**: Check Progress tab to identify areas needing focus
5. **Track Streaks**: Log hours daily to build study streak
6. **Use Search**: Find notes quickly with universal search
7. **Mock Tests**: Take practice tests to gauge readiness
8. **Flashcards**: AI can generate from your notes

---

## 🆘 Help Resources

**Installation Issues?** → See SETUP_GUIDE.md  
**Want to modify?** → See DEVELOPER_GUIDE.md  
**Deploying?** → See DEPLOYMENT.md  
**How something works?** → See IMPLEMENTATION_SUMMARY.md  
**Feature overview?** → See README.md

---

## 📞 Support

1. Check relevant documentation file
2. Review code comments in Python files
3. Check database schema in `database/db_init.py`
4. Review function docs in utility modules

---

**Version**: 1.0  
**Status**: Production Ready ✅  
**Last Updated**: June 2026

**Happy Studying! 📚✨**
