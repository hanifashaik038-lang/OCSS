import random
import sqlite3
from database.db_init import get_connection

def create_mock_test(subject_id, title, total_marks, num_questions, difficulty, test_type):
    """Create a new mock test"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO mock_tests 
        (subject_id, title, total_marks, num_questions, difficulty, test_type)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (subject_id, title, total_marks, num_questions, difficulty, test_type))
    
    conn.commit()
    test_id = cursor.lastrowid
    conn.close()
    return test_id

def get_mock_tests(subject_id=None):
    """Get all mock tests, optionally filtered by subject"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if subject_id:
        cursor.execute('''
            SELECT * FROM mock_tests 
            WHERE subject_id = ? 
            ORDER BY created_at DESC
        ''', (subject_id,))
    else:
        cursor.execute('SELECT * FROM mock_tests ORDER BY created_at DESC')
    
    tests = cursor.fetchall()
    conn.close()
    return tests

def update_test_score(test_id, obtained_marks):
    """Update the score for a mock test"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE mock_tests 
        SET obtained_marks = ? 
        WHERE id = ?
    ''', (obtained_marks, test_id))
    
    conn.commit()
    conn.close()

def generate_sample_questions(num_questions, difficulty, test_type):
    """Generate sample questions based on difficulty and type"""
    questions = []
    
    # Sample question templates
    mcq_questions = [
        {"q": "What is the capital of France?", "options": ["Paris", "London", "Berlin", "Madrid"], "answer": "Paris"},
        {"q": "Which planet is closest to the sun?", "options": ["Venus", "Mercury", "Earth", "Mars"], "answer": "Mercury"},
        {"q": "What is the chemical symbol for gold?", "options": ["Go", "Gd", "Au", "Ag"], "answer": "Au"},
    ]
    
    short_answer_questions = [
        {"q": "Define photosynthesis", "answer": "Process by which plants convert sunlight into chemical energy"},
        {"q": "What is the mitochondria?", "answer": "The powerhouse of the cell, responsible for energy production"},
    ]
    
    long_answer_questions = [
        {"q": "Explain the water cycle", "answer": "The water cycle involves evaporation, condensation, precipitation, and collection"},
        {"q": "Describe the theory of evolution", "answer": "Evolution is the process of change in all forms of life over time"},
    ]
    
    if test_type == "MCQ":
        available_q = mcq_questions
    elif test_type == "Short Answer":
        available_q = short_answer_questions
    elif test_type == "Long Answer":
        available_q = long_answer_questions
    else:  # Mixed
        available_q = mcq_questions + short_answer_questions + long_answer_questions
    
    # Select random questions
    selected = random.sample(available_q, min(num_questions, len(available_q)))
    
    for i, q in enumerate(selected, 1):
        questions.append({
            'number': i,
            'question': q['q'],
            'options': q.get('options', []),
            'answer': q['answer'],
            'type': test_type
        })
    
    return questions

def calculate_test_performance(total_marks, obtained_marks):
    """Calculate performance metrics"""
    if total_marks == 0:
        percentage = 0
    else:
        percentage = (obtained_marks / total_marks) * 100
    
    if percentage >= 80:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 40:
        grade = "C"
    else:
        grade = "D"
    
    return {
        'percentage': round(percentage, 2),
        'grade': grade,
        'obtained': obtained_marks,
        'total': total_marks
    }

def get_test_statistics(subject_id):
    """Get statistics for all tests in a subject"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            COUNT(*) as total_tests,
            AVG(CAST(obtained_marks AS FLOAT) / total_marks * 100) as avg_percentage,
            MAX(CAST(obtained_marks AS FLOAT) / total_marks * 100) as best_percentage,
            MIN(CAST(obtained_marks AS FLOAT) / total_marks * 100) as worst_percentage
        FROM mock_tests 
        WHERE subject_id = ?
    ''', (subject_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result[0] > 0:
        return {
            'total_tests': result[0],
            'avg_percentage': round(result[1], 2) if result[1] else 0,
            'best_percentage': round(result[2], 2) if result[2] else 0,
            'worst_percentage': round(result[3], 2) if result[3] else 0
        }
    return None
