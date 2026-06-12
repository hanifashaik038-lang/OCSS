import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from database.db_init import get_connection
from utils.analytics import get_dashboard_stats, calculate_weekly_streak, get_upcoming_deadlines, get_weak_topics

def show_dashboard():
    """Display the dashboard page"""
    st.set_page_config(page_title="Dashboard", layout="wide")
    
    st.title("📊 Study Dashboard")
    
    # Get overall statistics
    stats = get_dashboard_stats()
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Hours Studied", f"{stats['total_hours']}h", "📚")
    
    with col2:
        st.metric("Average Completion", f"{stats['avg_completion']:.1f}%", "✅")
    
    with col3:
        st.metric("Active Subjects", stats['num_subjects'], "📖")
    
    with col4:
        streak = calculate_weekly_streak()
        st.metric("Weekly Streak", f"{streak} days", "🔥")
    
    st.divider()
    
    # Recent activity section
    st.subheader("📌 Recent Activity")
    if stats['recent_activity']:
        for subject, updated_at in stats['recent_activity']:
            st.info(f"**{subject}** - Updated: {updated_at}")
    else:
        st.info("No recent activity yet. Start by adding a subject!")
    
    st.divider()
    
    # Upcoming exams section
    st.subheader("📅 Upcoming Exams")
    deadlines = get_upcoming_deadlines()
    
    if deadlines:
        for exam_id, exam_name, exam_date, subject in deadlines:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**{exam_name}** - {subject}")
            with col2:
                st.write(f"📆 {exam_date}")
            with col3:
                if st.button("View", key=f"exam_{exam_id}"):
                    st.session_state.selected_exam = exam_id
    else:
        st.info("No upcoming exams scheduled")
    
    st.divider()
    
    # Subject performance section
    st.subheader("📈 Subject Performance")
    
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
        subject_data = {
            'Subject': [],
            'Completion %': [],
            'Hours Studied': []
        }
        
        for subject_id, name, completion, hours in subjects:
            subject_data['Subject'].append(name)
            subject_data['Completion %'].append(completion or 0)
            subject_data['Hours Studied'].append(hours or 0)
        
        # Create completion chart
        fig = px.bar(
            x=subject_data['Subject'],
            y=subject_data['Completion %'],
            title="Subject Completion Progress",
            labels={'x': 'Subject', 'y': 'Completion %'},
            color=subject_data['Completion %'],
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Create hours studied chart
        fig2 = px.pie(
            values=subject_data['Hours Studied'],
            names=subject_data['Subject'],
            title="Study Time Distribution"
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No subjects added yet. Create a semester setup to get started!")

if __name__ == "__main__":
    show_dashboard()
