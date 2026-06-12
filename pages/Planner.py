import streamlit as st
from datetime import datetime, timedelta
from database.db_init import get_connection
from utils.planner import add_task, get_tasks, mark_task_complete, update_task, delete_task, generate_revision_schedule

def show_planner():
    """Display the planner page"""
    st.set_page_config(page_title="Planner", layout="wide")
    
    st.title("📅 Study Planner")
    
    # Get subjects
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM subjects ORDER BY name')
    subjects = cursor.fetchall()
    conn.close()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Calendar View", "Add Task", "Upcoming", "Revision Schedule"])
    
    with tab1:
        st.subheader("Calendar View")
        st.info("📅 Calendar view for tasks and exams")
        
        # Get all tasks and exams
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT due_date, title, 'Task' as type, priority
            FROM planner_tasks
            WHERE completed = 0
            UNION
            SELECT exam_date, name, 'Exam', 'High'
            FROM exams
        ''')
        events = cursor.fetchall()
        conn.close()
        
        if events:
            for event_date, title, event_type, priority in events:
                st.write(f"**[{event_type}]** {title} - {event_date} ({priority})")
        else:
            st.info("No upcoming events")
    
    with tab2:
        st.subheader("Add New Task")
        
        if not subjects:
            st.warning("Please add subjects first!")
        else:
            subject_options = {s[1]: s[0] for s in subjects}
            selected_subject_name = st.selectbox("Select Subject", list(subject_options.keys()))
            subject_id = subject_options[selected_subject_name]
            
            task_title = st.text_input("Task Title")
            task_description = st.text_area("Task Description")
            
            col1, col2 = st.columns(2)
            
            with col1:
                task_date = st.date_input("Due Date", value=datetime.now() + timedelta(days=7))
            
            with col2:
                priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            
            if st.button("Add Task", type="primary"):
                if task_title:
                    add_task(subject_id, task_title, task_description, str(task_date), priority)
                    st.success("✅ Task added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a task title")
    
    with tab3:
        st.subheader("Upcoming Tasks (Next 7 Days)")
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pt.id, pt.title, pt.due_date, pt.priority, s.name, pt.completed
            FROM planner_tasks pt
            JOIN subjects s ON pt.subject_id = s.id
            WHERE pt.due_date >= DATE('now')
            AND pt.due_date <= DATE('now', '+7 days')
            AND pt.completed = 0
            ORDER BY pt.due_date ASC
        ''')
        
        tasks = cursor.fetchall()
        conn.close()
        
        if tasks:
            for task_id, title, due_date, priority, subject, completed in tasks:
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{title}**")
                        st.caption(f"{subject}")
                    
                    with col2:
                        priority_color = "🔴" if priority == "High" else "🟡" if priority == "Medium" else "🟢"
                        st.write(f"{priority_color} {priority}")
                    
                    with col3:
                        st.write(f"📅 {due_date}")
                    
                    with col4:
                        if st.button("✓ Done", key=f"mark_done_{task_id}"):
                            mark_task_complete(task_id)
                            st.rerun()
        else:
            st.info("No upcoming tasks for the next 7 days")
    
    with tab4:
        st.subheader("Generate Revision Schedule")
        
        if not subjects:
            st.warning("Please add subjects first!")
        else:
            subject_options = {s[1]: s[0] for s in subjects}
            selected_subject_name = st.selectbox("Select Subject for Revision", list(subject_options.keys()), key="revision_subject")
            subject_id = subject_options[selected_subject_name]
            
            # Get exams for this subject
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, exam_date, marks
                FROM exams
                WHERE subject_id = ?
                ORDER BY exam_date
            ''', (subject_id,))
            exams = cursor.fetchall()
            conn.close()
            
            if exams:
                selected_exam_id = st.selectbox(
                    "Select Exam",
                    options=[e[0] for e in exams],
                    format_func=lambda x: f"{[e[1] for e in exams if e[0] == x][0]} - {[e[2] for e in exams if e[0] == x][0]}"
                )
                
                exam_name = next(e[1] for e in exams if e[0] == selected_exam_id)
                exam_date = next(e[2] for e in exams if e[0] == selected_exam_id)
                
                num_sessions = st.slider("Number of Revision Sessions", 5, 20, 10)
                
                if st.button("Generate Schedule", type="primary"):
                    schedule = generate_revision_schedule(exam_date, subject_id, num_sessions)
                    
                    if schedule:
                        st.success(f"✅ Generated {len(schedule)} revision sessions!")
                        
                        for session in schedule:
                            st.write(f"**Session {session['session']}** - {session['date']}")
                    else:
                        st.warning("Exam date is in the past!")
            else:
                st.info("Add exams for this subject to generate revision schedule")

if __name__ == "__main__":
    show_planner()
