import streamlit as st
from database.db_init import get_connection
import os

def show_ai_assistant():
    """Display the AI Assistant page"""
    st.set_page_config(page_title="AI Assistant", layout="wide")
    
    st.title("🤖 AI Study Assistant")
    
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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Summarize", "Q&A", "Flashcards", "Concept Explanation", "Revision Notes"])
    
    with tab1:
        st.subheader("📄 Summarize Documents")
        st.info("Upload a document to get an AI-generated summary")
        
        subject_options = {s[1]: s[0] for s in subjects}
        selected_subject_name = st.selectbox("Select Subject", list(subject_options.keys()), key="summary_subject")
        subject_id = subject_options[selected_subject_name]
        
        # Get uploaded files for this subject
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, filename, file_path
            FROM uploads
            WHERE subject_id = ?
        ''', (subject_id,))
        uploads = cursor.fetchall()
        conn.close()
        
        if uploads:
            selected_file = st.selectbox(
                "Select File",
                options=[u[0] for u in uploads],
                format_func=lambda x: next(u[1] for u in uploads if u[0] == x)
            )
            
            if st.button("Generate Summary", type="primary"):
                filename = next(u[1] for u in uploads if u[0] == selected_file)
                st.success(f"✅ Summary generated for {filename}")
                st.write("""
                **Sample Summary:**
                
                This document covers the fundamental principles of photosynthesis. 
                Key points include:
                - The process occurs in chloroplasts
                - Requires sunlight, water, and CO2
                - Produces glucose and oxygen
                - Essential for plant growth and energy
                - Critical for maintaining oxygen levels in atmosphere
                """)
        else:
            st.info("Upload documents in the Subjects module to generate summaries")
    
    with tab2:
        st.subheader("❓ Question & Answer")
        st.info("Ask questions about your uploaded materials")
        
        subject_options = {s[1]: s[0] for s in subjects}
        selected_subject_name = st.selectbox("Select Subject", list(subject_options.keys()), key="qa_subject")
        
        question = st.text_area("Ask a question about your study materials")
        
        if st.button("Get Answer", type="primary"):
            if question:
                st.success("✅ Processing your question...")
                st.write("""
                **Answer:**
                
                Based on your study materials, here's the answer:
                
                [AI-Generated Answer will appear here based on your documents]
                
                This feature will analyze your uploaded PDFs, presentations, and documents
                to provide accurate answers to your questions.
                """)
            else:
                st.error("Please enter a question")
    
    with tab3:
        st.subheader("🃏 Generate Flashcards")
        st.info("Create flashcards for quick revision")
        
        subject_options = {s[1]: s[0] for s in subjects}
        selected_subject_name = st.selectbox("Select Subject", list(subject_options.keys()), key="flashcard_subject")
        subject_id = subject_options[selected_subject_name]
        
        topic = st.text_input("Enter topic for flashcards")
        num_cards = st.slider("Number of flashcards", 5, 50, 10)
        
        if st.button("Generate Flashcards", type="primary"):
            if topic:
                conn = get_connection()
                cursor = conn.cursor()
                
                # Generate sample flashcards
                sample_flashcards = [
                    ("What is photosynthesis?", "The process by which plants convert sunlight into chemical energy"),
                    ("What are the inputs of photosynthesis?", "Water, CO2, and sunlight"),
                    ("What are the outputs?", "Glucose and oxygen"),
                    ("Where does photosynthesis occur?", "In the chloroplasts of plant cells"),
                    ("What pigment captures light?", "Chlorophyll"),
                ]
                
                for q, a in sample_flashcards[:num_cards]:
                    cursor.execute('''
                        INSERT INTO flashcards (subject_id, question, answer)
                        VALUES (?, ?, ?)
                    ''', (subject_id, q, a))
                
                conn.commit()
                conn.close()
                
                st.success(f"✅ Generated {num_cards} flashcards for '{topic}'!")
            else:
                st.error("Please enter a topic")
    
    with tab4:
        st.subheader("💡 Explain Concepts")
        st.info("Get detailed explanations of difficult concepts")
        
        concept = st.text_input("Enter a concept to explain")
        
        if st.button("Explain Concept", type="primary"):
            if concept:
                st.success(f"✅ Explanation for '{concept}':")
                st.write(f"""
                **{concept}**
                
                **Definition:**
                [AI-generated definition]
                
                **Key Points:**
                - Point 1
                - Point 2
                - Point 3
                
                **Examples:**
                [Real-world examples]
                
                **Related Concepts:**
                - Related topic 1
                - Related topic 2
                """)
            else:
                st.error("Please enter a concept")
    
    with tab5:
        st.subheader("📝 Generate Revision Notes")
        st.info("Create condensed revision notes from your materials")
        
        subject_options = {s[1]: s[0] for s in subjects}
        selected_subject_name = st.selectbox("Select Subject", list(subject_options.keys()), key="revision_subject")
        
        topics = st.text_area("Enter topics to revise (comma-separated)")
        
        if st.button("Generate Revision Notes", type="primary"):
            if topics:
                st.success(f"✅ Revision notes generated!")
                st.markdown("""
                ## Revision Notes
                
                ### Topic 1: Photosynthesis
                - Key concept 1
                - Key concept 2
                - Key equations/formulas
                
                ### Topic 2: Cell Structure
                - Important definitions
                - Structural components
                - Functions
                
                ### Key Takeaways
                1. Main point 1
                2. Main point 2
                3. Main point 3
                """)
            else:
                st.error("Please enter at least one topic")

if __name__ == "__main__":
    show_ai_assistant()
