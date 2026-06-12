import streamlit as st
from database.db_init import get_connection
from utils.quiz_generator import create_mock_test, get_mock_tests, update_test_score, generate_sample_questions, calculate_test_performance, get_test_statistics

def show_mock_tests():
    """Display the mock tests page"""
    st.set_page_config(page_title="Mock Tests", layout="wide")
    
    st.title("✅ Mock Tests")
    
    # Get subjects
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM subjects ORDER BY name')
    subjects = cursor.fetchall()
    conn.close()
    
    if not subjects:
        st.warning("Please add subjects first!")
        return
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Create Test", "My Tests", "Statistics"])
    
    with tab1:
        st.subheader("Create New Mock Test")
        
        subject_options = {s[1]: s[0] for s in subjects}
        selected_subject_name = st.selectbox("Select Subject", list(subject_options.keys()))
        subject_id = subject_options[selected_subject_name]
        
        col1, col2 = st.columns(2)
        
        with col1:
            test_title = st.text_input("Test Title")
            num_questions = st.number_input("Number of Questions", 5, 100, 10)
        
        with col2:
            total_marks = st.number_input("Total Marks", 10, 500, 100)
            difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
        
        test_type = st.selectbox("Test Type", ["MCQ", "Short Answer", "Long Answer", "Mixed"])
        
        if st.button("Generate Test", type="primary"):
            if test_title:
                test_id = create_mock_test(subject_id, test_title, total_marks, num_questions, difficulty, test_type)
                st.success(f"✅ Test created with ID: {test_id}")
                st.session_state.current_test_id = test_id
                st.rerun()
            else:
                st.error("Please enter a test title")
    
    with tab2:
        st.subheader("My Mock Tests")
        
        subject_options = {s[1]: s[0] for s in subjects}
        selected_subject_name = st.selectbox("Filter by Subject", ["All"] + list(subject_options.keys()), key="test_subject_filter")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        if selected_subject_name == "All":
            cursor.execute('''
                SELECT mt.id, mt.title, mt.total_marks, mt.obtained_marks, mt.num_questions, mt.difficulty, mt.test_type, s.name
                FROM mock_tests mt
                JOIN subjects s ON mt.subject_id = s.id
                ORDER BY mt.created_at DESC
            ''')
        else:
            subject_id = subject_options[selected_subject_name]
            cursor.execute('''
                SELECT mt.id, mt.title, mt.total_marks, mt.obtained_marks, mt.num_questions, mt.difficulty, mt.test_type, s.name
                FROM mock_tests mt
                JOIN subjects s ON mt.subject_id = s.id
                WHERE mt.subject_id = ?
                ORDER BY mt.created_at DESC
            ''', (subject_id,))
        
        tests = cursor.fetchall()
        conn.close()
        
        if tests:
            for test_id, title, total_marks, obtained_marks, num_questions, difficulty, test_type, subject in tests:
                with st.container(border=True):
                    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1, 1])
                    
                    with col1:
                        st.write(f"**{title}**")
                        st.caption(f"{subject} | {difficulty}")
                    
                    with col2:
                        st.write(f"Questions: {num_questions}")
                    
                    with col3:
                        if obtained_marks is not None:
                            percentage = (obtained_marks / total_marks) * 100
                            st.metric("Score", f"{obtained_marks}/{total_marks} ({percentage:.1f}%)")
                        else:
                            st.write("Not Attempted")
                    
                    with col4:
                        if st.button("Attempt", key=f"attempt_{test_id}"):
                            st.session_state.current_test_id = test_id
                    
                    with col5:
                        if st.button("Delete", key=f"del_test_{test_id}"):
                            delete_test(test_id)
                            st.rerun()
        else:
            st.info("No tests created yet")
    
    with tab3:
        st.subheader("Test Statistics")
        
        subject_options = {s[1]: s[0] for s in subjects}
        selected_subject_name = st.selectbox("Select Subject", list(subject_options.keys()), key="stats_subject")
        subject_id = subject_options[selected_subject_name]
        
        stats = get_test_statistics(subject_id)
        
        if stats:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Tests", stats['total_tests'])
            
            with col2:
                st.metric("Average Score", f"{stats['avg_percentage']:.1f}%")
            
            with col3:
                st.metric("Best Score", f"{stats['best_percentage']:.1f}%")
            
            with col4:
                st.metric("Worst Score", f"{stats['worst_percentage']:.1f}%")
        else:
            st.info("No test data available for this subject")

def delete_test(test_id):
    """Delete a mock test"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM mock_tests WHERE id = ?', (test_id,))
    conn.commit()
    conn.close()
    st.success("✅ Test deleted")

if __name__ == "__main__":
    show_mock_tests()
