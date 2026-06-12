import streamlit as st
import os
from datetime import datetime, timedelta
from database.db_init import init_database, get_connection
from utils.file_manager import create_subject_folder, save_uploaded_file
from utils.planner import generate_revision_schedule

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    init_database()
    st.session_state.initialized = True

# Page configuration
st.set_page_config(
    page_title="OCSS - Online Collaborative Study System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📚 OCSS")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "⚙️ Setup",
        "📖 Subjects",
        "📝 Notes",
        "📅 Planner",
        "✅ Mock Tests",
        "📊 Progress",
        "🤖 AI Assistant",
        "📤 Uploads"
    ]
)

st.sidebar.divider()

# About section
st.sidebar.subheader("About OCSS")
st.sidebar.info(
    """
    **Online Collaborative Study System**
    
    A comprehensive platform for managing your studies with:
    - 📚 Subject management
    - 📝 Note-taking
    - 📅 Study planning
    - ✅ Mock tests
    - 📊 Progress tracking
    - 🤖 AI study assistance
    """
)

# Main content based on selected page
if page == "🏠 Home":
    show_home()
elif page == "⚙️ Setup":
    show_setup()
elif page == "📖 Subjects":
    from pages.Subjects import show_subjects
    show_subjects()
elif page == "📝 Notes":
    from pages.Notes import show_notes
    show_notes()
elif page == "📅 Planner":
    from pages.Planner import show_planner
    show_planner()
elif page == "✅ Mock Tests":
    from pages.Mock_Tests import show_mock_tests
    show_mock_tests()
elif page == "📊 Progress":
    from pages.Progress import show_progress
    show_progress()
elif page == "🤖 AI Assistant":
    from pages.AI_Assistant import show_ai_assistant
    show_ai_assistant()
elif page == "📤 Uploads":
    show_uploads()


def show_home():
    """Display the home page"""
    st.title("🎓 Welcome to OCSS")
    
    st.markdown("""
    ## Online Collaborative Study System
    
    Your complete study companion for managing semesters, subjects, and exams.
    """)
    
    st.divider()
    
    # Quick statistics
    col1, col2, col3, col4 = st.columns(4)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) FROM semesters')
    num_semesters = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM subjects')
    num_subjects = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM exams')
    num_exams = cursor.fetchone()[0]
    
    cursor.execute('SELECT COALESCE(SUM(hours_studied), 0) FROM progress')
    total_hours = cursor.fetchone()[0]
    
    conn.close()
    
    with col1:
        st.metric("📅 Semesters", num_semesters)
    with col2:
        st.metric("📚 Subjects", num_subjects)
    with col3:
        st.metric("🎯 Exams", num_exams)
    with col4:
        st.metric("⏱️ Hours Studied", f"{total_hours:.1f}")
    
    st.divider()
    
    # Getting started section
    st.subheader("🚀 Getting Started")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Step 1: Setup Your Semester
        Go to **Setup** to create your first semester with:
        - Semester name
        - Subject list
        - Exam dates
        """)
    
    with col2:
        st.markdown("""
        ### Step 2: Start Adding Notes
        Use the **Notes** section to:
        - Create rich-text notes
        - Organize by subject
        - Search across notes
        """)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        ### Step 3: Plan Your Studies
        Use the **Planner** to:
        - Schedule study sessions
        - Track assignments
        - Set exam reminders
        """)
    
    with col4:
        st.markdown("""
        ### Step 4: Test Yourself
        Visit **Mock Tests** to:
        - Create practice tests
        - Track your performance
        - Identify weak topics
        """)
    
    st.divider()
    
    # Features section
    st.subheader("✨ Key Features")
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.success("📁 **File Management**\nUpload and organize PDFs, presentations, and documents")
    
    with feature_col2:
        st.info("🎯 **Mock Tests**\nGenerate practice tests and track performance")
    
    with feature_col3:
        st.warning("📊 **Analytics**\nTrack progress and identify areas to focus on")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.success("📝 **Note Taking**\nRich-text editor with auto-save functionality")
    
    with col5:
        st.info("🤖 **AI Assistant**\nSummarize documents and generate flashcards")
    
    with col6:
        st.warning("📅 **Smart Planning**\nAutomated revision schedules and reminders")


def show_setup():
    """Display the semester setup page"""
    st.title("⚙️ Semester Setup")
    
    st.markdown("""
    ### Step 1: One-Click Semester Setup
    
    Create a new semester with all subjects and exams in one go!
    """)
    
    st.divider()
    
    # Tab for creating new semester
    tab1, tab2 = st.tabs(["Create New Semester", "View Semesters"])
    
    with tab1:
        st.subheader("Create New Semester")
        
        col1, col2 = st.columns(2)
        
        with col1:
            semester_name = st.text_input("Semester Name (e.g., Fall 2024)")
        
        with col2:
            start_date = st.date_input("Semester Start Date")
        
        end_date = st.date_input("Semester End Date")
        
        st.subheader("Add Subjects")
        
        num_subjects = st.number_input("Number of subjects", min_value=1, max_value=20, value=3)
        
        subjects = []
        exams = {}
        
        for i in range(num_subjects):
            st.write(f"**Subject {i+1}**")
            col1, col2 = st.columns(2)
            
            with col1:
                subject_name = st.text_input(f"Subject Name {i+1}")
            
            with col2:
                exam_date = st.date_input(f"Exam Date {i+1}", key=f"exam_date_{i}")
            
            col3, col4 = st.columns(2)
            
            with col3:
                exam_marks = st.number_input(f"Total Marks {i+1}", value=100)
            
            if subject_name:
                subjects.append(subject_name)
                exams[subject_name] = {
                    'date': str(exam_date),
                    'marks': exam_marks
                }
        
        st.divider()
        
        if st.button("Create Semester Setup", type="primary"):
            if semester_name and subjects:
                conn = get_connection()
                cursor = conn.cursor()
                
                # Create semester
                cursor.execute('''
                    INSERT INTO semesters (name, start_date, end_date)
                    VALUES (?, ?, ?)
                ''', (semester_name, str(start_date), str(end_date)))
                
                semester_id = cursor.lastrowid
                
                # Create subjects and exams
                for subject_name in subjects:
                    # Create subject folder
                    subject_folder = create_subject_folder(subject_name, semester_name)
                    
                    # Add subject to database
                    cursor.execute('''
                        INSERT INTO subjects (semester_id, name, folder_path)
                        VALUES (?, ?, ?)
                    ''', (semester_id, subject_name, subject_folder))
                    
                    subject_id = cursor.lastrowid
                    
                    # Initialize progress
                    cursor.execute('''
                        INSERT INTO progress (subject_id, hours_studied, completion_percentage)
                        VALUES (?, 0, 0)
                    ''', (subject_id,))
                    
                    # Add exam
                    exam_info = exams[subject_name]
                    cursor.execute('''
                        INSERT INTO exams (subject_id, name, exam_date, marks)
                        VALUES (?, ?, ?, ?)
                    ''', (subject_id, f"{subject_name} Exam", exam_info['date'], exam_info['marks']))
                    
                    # Generate revision schedule
                    generate_revision_schedule(exam_info['date'], subject_id)
                
                conn.commit()
                conn.close()
                
                st.success(f"✅ Semester '{semester_name}' created successfully!")
                st.balloons()
                st.rerun()
            else:
                st.error("Please fill in all required fields")
    
    with tab2:
        st.subheader("Your Semesters")
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.id, s.name, s.start_date, s.end_date, COUNT(sub.id) as subject_count
            FROM semesters s
            LEFT JOIN subjects sub ON s.id = sub.semester_id
            GROUP BY s.id
            ORDER BY s.start_date DESC
        ''')
        
        semesters = cursor.fetchall()
        conn.close()
        
        if semesters:
            for sem_id, name, start_date, end_date, subject_count in semesters:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1.5, 1])
                    
                    with col1:
                        st.write(f"**{name}**")
                        st.caption(f"{start_date} to {end_date}")
                    
                    with col2:
                        st.write(f"📚 {subject_count} subjects")
                    
                    with col3:
                        if st.button("View", key=f"view_sem_{sem_id}"):
                            st.session_state.selected_semester = sem_id
        else:
            st.info("No semesters created yet. Create one above!")


def show_uploads():
    """Display the uploads management page"""
    st.title("📤 File Uploads")
    
    st.markdown("""
    Upload your study materials - PDFs, presentations, documents, and images.
    Organize them by subject for easy access.
    """)
    
    st.divider()
    
    # Get subjects
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, folder_path FROM subjects ORDER BY name')
    subjects = cursor.fetchall()
    conn.close()
    
    if not subjects:
        st.warning("Please add subjects first!")
        return
    
    # Tabs
    tab1, tab2 = st.tabs(["Upload Files", "View Files"])
    
    with tab1:
        st.subheader("Upload New Files")
        
        subject_options = {s[1]: (s[0], s[2]) for s in subjects}
        selected_subject_name = st.selectbox("Select Subject", list(subject_options.keys()))
        subject_id, subject_folder = subject_options[selected_subject_name]
        
        uploaded_files = st.file_uploader(
            "Choose files to upload",
            type=['pdf', 'pptx', 'docx', 'png', 'jpg', 'jpeg', 'gif'],
            accept_multiple_files=True
        )
        
        if st.button("Upload Files", type="primary"):
            if uploaded_files:
                conn = get_connection()
                cursor = conn.cursor()
                
                for uploaded_file in uploaded_files:
                    # Save file
                    file_path = save_uploaded_file(uploaded_file, subject_folder)
                    
                    # Add to database
                    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
                    cursor.execute('''
                        INSERT INTO uploads (subject_id, filename, file_path, file_type)
                        VALUES (?, ?, ?, ?)
                    ''', (subject_id, uploaded_file.name, file_path, file_ext))
                
                conn.commit()
                conn.close()
                
                st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
                st.rerun()
            else:
                st.error("Please select at least one file")
    
    with tab2:
        st.subheader("Your Files")
        
        subject_options_view = {s[1]: s[0] for s in subjects}
        selected_subject_name_view = st.selectbox(
            "Filter by Subject",
            ["All"] + list(subject_options_view.keys()),
            key="view_files_subject"
        )
        
        conn = get_connection()
        cursor = conn.cursor()
        
        if selected_subject_name_view == "All":
            cursor.execute('''
                SELECT u.id, u.filename, u.file_type, s.name, u.upload_date
                FROM uploads u
                JOIN subjects s ON u.subject_id = s.id
                ORDER BY u.upload_date DESC
            ''')
        else:
            subject_id = subject_options_view[selected_subject_name_view]
            cursor.execute('''
                SELECT u.id, u.filename, u.file_type, s.name, u.upload_date
                FROM uploads u
                JOIN subjects s ON u.subject_id = s.id
                WHERE u.subject_id = ?
                ORDER BY u.upload_date DESC
            ''', (subject_id,))
        
        files = cursor.fetchall()
        conn.close()
        
        if files:
            for file_id, filename, file_type, subject, upload_date in files:
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 0.5])
                    
                    with col1:
                        st.write(f"📄 **{filename}**")
                        st.caption(f"{subject}")
                    
                    with col2:
                        st.write(f"Type: {file_type}")
                    
                    with col3:
                        st.caption(f"📅 {upload_date}")
                    
                    with col4:
                        if st.button("Delete", key=f"del_upload_{file_id}"):
                            conn = get_connection()
                            cursor = conn.cursor()
                            cursor.execute('DELETE FROM uploads WHERE id = ?', (file_id,))
                            conn.commit()
                            conn.close()
                            st.rerun()
        else:
            st.info("No files uploaded yet")


if __name__ == "__main__":
    pass
