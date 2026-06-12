import streamlit as st
from datetime import datetime
from database.db_init import get_connection

def show_notes():
    """Display the notes page"""
    st.set_page_config(page_title="Notes", layout="wide")
    
    st.title("📝 Notes")
    
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
    tab1, tab2, tab3 = st.tabs(["View Notes", "Create Note", "Search"])
    
    with tab1:
        st.subheader("My Notes")
        
        subject_options = {s[1]: s[0] for s in subjects}
        selected_subject_name = st.selectbox("Filter by Subject", ["All"] + list(subject_options.keys()))
        
        conn = get_connection()
        cursor = conn.cursor()
        
        if selected_subject_name == "All":
            cursor.execute('''
                SELECT n.id, n.title, n.content, n.created_at, s.name
                FROM notes n
                JOIN subjects s ON n.subject_id = s.id
                ORDER BY n.created_at DESC
            ''')
        else:
            subject_id = subject_options[selected_subject_name]
            cursor.execute('''
                SELECT n.id, n.title, n.content, n.created_at, s.name
                FROM notes n
                JOIN subjects s ON n.subject_id = s.id
                WHERE n.subject_id = ?
                ORDER BY n.created_at DESC
            ''', (subject_id,))
        
        notes = cursor.fetchall()
        conn.close()
        
        if notes:
            for note_id, title, content, created_at, subject in notes:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1.5, 1])
                    
                    with col1:
                        st.write(f"**{title}**")
                        st.caption(f"Subject: {subject}")
                    
                    with col2:
                        st.caption(f"📅 {created_at}")
                    
                    with col3:
                        if st.button("Edit", key=f"edit_{note_id}"):
                            st.session_state.edit_note_id = note_id
                        if st.button("Delete", key=f"del_note_{note_id}"):
                            delete_note(note_id)
                            st.rerun()
                    
                    if st.button("View", key=f"view_note_{note_id}"):
                        st.session_state.view_note_id = note_id
                    
                    # Show preview
                    preview = content[:200] + "..." if len(content) > 200 else content
                    st.text_area("Preview", value=preview, disabled=True, height=100, key=f"preview_{note_id}")
        else:
            st.info("No notes yet. Create one to get started!")
    
    with tab2:
        st.subheader("Create New Note")
        
        subject_options = {s[1]: s[0] for s in subjects}
        selected_subject_name = st.selectbox("Select Subject", list(subject_options.keys()), key="new_note_subject")
        subject_id = subject_options[selected_subject_name]
        
        note_title = st.text_input("Note Title")
        note_content = st.text_area("Note Content", height=300, placeholder="Write your notes here...")
        
        if st.button("Save Note", type="primary"):
            if note_title and note_content:
                conn = get_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO notes (subject_id, title, content, created_at, updated_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ''', (subject_id, note_title, note_content))
                
                conn.commit()
                conn.close()
                
                st.success("✅ Note saved successfully!")
                st.rerun()
            else:
                st.error("Please fill in all fields")
    
    with tab3:
        st.subheader("Search Notes")
        
        search_query = st.text_input("Search in notes")
        
        if search_query:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT n.id, n.title, n.content, s.name
                FROM notes n
                JOIN subjects s ON n.subject_id = s.id
                WHERE n.title LIKE ? OR n.content LIKE ?
                ORDER BY n.created_at DESC
            ''', (f"%{search_query}%", f"%{search_query}%"))
            
            results = cursor.fetchall()
            conn.close()
            
            if results:
                st.success(f"Found {len(results)} result(s)")
                for note_id, title, content, subject in results:
                    with st.container(border=True):
                        st.write(f"**{title}** ({subject})")
                        preview = content[:150] + "..." if len(content) > 150 else content
                        st.caption(preview)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("View", key=f"search_view_{note_id}"):
                                st.session_state.view_note_id = note_id
                        with col2:
                            if st.button("Delete", key=f"search_del_{note_id}"):
                                delete_note(note_id)
                                st.rerun()
            else:
                st.info("No notes found matching your search")

def delete_note(note_id):
    """Delete a note"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    st.success("✅ Note deleted")

if __name__ == "__main__":
    show_notes()
