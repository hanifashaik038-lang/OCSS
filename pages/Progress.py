import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from database.db_init import get_connection
from utils.analytics import get_weak_topics, get_dashboard_stats

def show_progress():
    """Display the progress page"""
    st.set_page_config(page_title="Progress", layout="wide")
    
    st.title("📊 Progress & Analytics")
    
    # Get subjects
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM subjects ORDER BY name')
    subjects = cursor.fetchall()
    conn.close()
    
    if not subjects:
        st.warning("Please add subjects first!")
        return
    
    # Overall statistics
    st.subheader("📈 Overall Statistics")
    
    stats = get_dashboard_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Hours Studied", f"{stats['total_hours']}h")
    
    with col2:
        st.metric("Subjects Tracked", stats['num_subjects'])
    
    with col3:
        st.metric("Average Completion", f"{stats['avg_completion']:.1f}%")
    
    with col4:
        from utils.analytics import calculate_weekly_streak
        streak = calculate_weekly_streak()
        st.metric("Weekly Streak", f"{streak} days")
    
    st.divider()
    
    # Subject-wise progress
    st.subheader("📚 Subject-wise Progress")
    
    subject_options = {s[1]: s[0] for s in subjects}
    selected_subject_name = st.selectbox("Select Subject", list(subject_options.keys()))
    subject_id = subject_options[selected_subject_name]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.hours_studied, p.completion_percentage, p.revision_status
        FROM progress p
        WHERE p.subject_id = ?
    ''', (subject_id,))
    
    progress_data = cursor.fetchone()
    
    if progress_data:
        hours, completion, revision_status = progress_data
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Hours Studied", f"{hours:.1f}h")
        
        with col2:
            st.metric("Completion", f"{completion:.1f}%")
        
        with col3:
            st.metric("Revision Status", revision_status)
    
    # Revision timeline
    st.subheader("📅 Revision Timeline")
    
    cursor.execute('''
        SELECT id, title, due_date, priority, completed
        FROM planner_tasks
        WHERE subject_id = ?
        ORDER BY due_date ASC
    ''', (subject_id,))
    
    tasks = cursor.fetchall()
    
    if tasks:
        # Create a timeline visualization
        timeline_data = []
        for task_id, title, due_date, priority, completed in tasks:
            status = "✓ Completed" if completed else "⏳ Pending"
            timeline_data.append({
                'Task': title,
                'Date': due_date,
                'Priority': priority,
                'Status': status
            })
        
        for item in timeline_data:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{item['Task']}**")
            with col2:
                st.write(item['Date'])
            with col3:
                st.write(item['Status'])
    
    # Mock test performance
    st.subheader("🎯 Mock Test Performance")
    
    cursor.execute('''
        SELECT id, title, total_marks, obtained_marks, difficulty
        FROM mock_tests
        WHERE subject_id = ?
        ORDER BY created_at DESC
    ''', (subject_id,))
    
    tests = cursor.fetchall()
    conn.close()
    
    if tests:
        performance_data = {
            'Test': [],
            'Score': [],
            'Difficulty': []
        }
        
        for test_id, title, total_marks, obtained_marks, difficulty in tests:
            if obtained_marks is not None:
                percentage = (obtained_marks / total_marks) * 100
                performance_data['Test'].append(title)
                performance_data['Score'].append(percentage)
                performance_data['Difficulty'].append(difficulty)
        
        if performance_data['Test']:
            fig = px.bar(
                x=performance_data['Test'],
                y=performance_data['Score'],
                title="Mock Test Performance",
                labels={'x': 'Test', 'y': 'Percentage Score'},
                color=performance_data['Difficulty'],
                color_discrete_map={'Easy': '#00CC96', 'Medium': '#FFA15A', 'Hard': '#EF553B'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No completed tests yet")
    else:
        st.info("No mock tests for this subject")
    
    # Weak topics analysis
    st.subheader("⚠️ Areas to Focus On")
    
    weak_topics = get_weak_topics(subject_id)
    
    if weak_topics:
        for topic in weak_topics:
            with st.container(border=True):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**{topic['topic']}**")
                with col2:
                    st.metric("Avg Score", f"{topic['score']:.1f}%")
    else:
        st.success("✅ No weak topics identified! Keep up the good work!")

if __name__ == "__main__":
    show_progress()
