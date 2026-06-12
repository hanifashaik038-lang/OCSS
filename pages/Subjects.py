import streamlit as st
from database.db_init import get_connection
from utils.file_manager import create_subject_folder
from utils.planner import generate_revision_schedule

def show_subjects():
    """Display the subjects page"""
    st.set_page_config(page_title="Subjects", layout="wide")
    
    st.title("📖 Subjects")
    
    # Tabs for different actions
    tab1, tab2, tab3 = st.tabs(["View Subjects", "Add Subject", "Manage"])
    
    with tab1:
        st.subheader("My Subjects")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.id, s.name, sem.name as semester, p.completion_percentage, p.hours_studied
            FROM subjects s
            LEFT JOIN semesters sem ON s.semester_id = sem.id
            LEFT JOIN progress p ON s.id = p.subject_id
            ORDER BY sem.name, s.name
        ''')
        
        subjects = cursor.fetchall()
        conn.close()
        
        if subjects:
            for subject_id, name, semester, completion, hours in subjects:
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1, 1.5])
                    
                    with col1:
                        st.write(f"**{name}**")
                        st.caption(f"Semester: {semester}")
                    
                    with col2:
                        st.metric("Completion", f"{completion or 0:.0f}%")
                    
                    with col3:
                        st.metric("Hours", f"{hours or 0:.1f}h")
                    
                    with col4:
                        if st.button("View", key=f"view_{subject_id}"):
                            st.session_state.selected_subject = subject_id
                    
                    with col5:
                        if st.button("Delete", key=f"del_{subject_id}"):
                            delete_subject(subject_id)
                            st.rerun()
                    
                    st.divider()
        else:
            st.info("No subjects added yet. Create a semester setup first!")
    
    with tab2:
        st.subheader("Add New Subject")
        
        # Get available semesters
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM semesters ORDER BY name')
        semesters = cursor.fetchall()
        conn.close()
        
        if not semesters:
            st.warning("Please create a semester first!")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                semester_options = {sem[1]: sem[0] for sem in semesters}
                selected_semester_name = st.selectbox("Select Semester", semester_options.keys())
                semester_id = semester_options[selected_semester_name]
            
            with col2:
                subject_name = st.text_input("Subject Name")
            
            if st.button("Add Subject", type="primary"):
                if subject_name:
                    conn = get_connection()
                    cursor = conn.cursor()
                    
                    # Create subject folder
                    subject_folder = create_subject_folder(subject_name, selected_semester_name)
                    
                    # Add to database
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
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"✅ Subject '{subject_name}' added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a subject name")
    
    with tab3:
        st.subheader("Subject Management")
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.id, s.name, p.completion_percentage, p.hours_studied
            FROM subjects s
            LEFT JOIN progress p ON s.id = p.subject_id
        ''')
        subjects = cursor.fetchall()
        conn.close()
        
        if subjects:
            selected_subject = st.selectbox(
                "Select Subject",
                options=[s[0] for s in subjects],
                format_func=lambda x: next(s[1] for s in subjects if s[0] == x)
            )
            
            subject_name = next(s[1] for s in subjects if s[0] == selected_subject)
            
            st.subheader(f"Manage: {subject_name}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                hours = st.number_input("Add Study Hours", value=0.0, min_value=0.0, step=0.5)
                if st.button("Log Hours"):
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE progress 
                        SET hours_studied = hours_studied + ?
                        WHERE subject_id = ?
                    ''', (hours, selected_subject))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Added {hours} hours")
                    st.rerun()
            
            with col2:
                completion = st.slider("Completion %", 0, 100, 0)
                if st.button("Update Progress"):
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE progress 
                        SET completion_percentage = ?
                        WHERE subject_id = ?
                    ''', (completion, selected_subject))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Updated completion to {completion}%")
                    st.rerun()
        else:
            st.info("No subjects to manage")

def delete_subject(subject_id):
    """Delete a subject"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM subjects WHERE id = ?', (subject_id,))
    cursor.execute('DELETE FROM progress WHERE subject_id = ?', (subject_id,))
    cursor.execute('DELETE FROM exams WHERE subject_id = ?', (subject_id,))
    cursor.execute('DELETE FROM uploads WHERE subject_id = ?', (subject_id,))
    cursor.execute('DELETE FROM notes WHERE subject_id = ?', (subject_id,))
    cursor.execute('DELETE FROM planner_tasks WHERE subject_id = ?', (subject_id,))
    cursor.execute('DELETE FROM mock_tests WHERE subject_id = ?', (subject_id,))
    
    conn.commit()
    conn.close()
    st.success("Subject deleted successfully")

if __name__ == "__main__":
    show_subjects()
