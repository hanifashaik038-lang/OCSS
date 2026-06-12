import sqlite3
from datetime import datetime, timedelta
from database.db_init import get_connection

def update_study_hours(subject_id, hours):
    """Update study hours for a subject"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id FROM progress WHERE subject_id = ?
    ''', (subject_id,))
    
    result = cursor.fetchone()
    
    if result:
        cursor.execute('''
            UPDATE progress 
            SET hours_studied = hours_studied + ?, updated_at = CURRENT_TIMESTAMP
            WHERE subject_id = ?
        ''', (hours, subject_id))
    else:
        cursor.execute('''
            INSERT INTO progress (subject_id, hours_studied)
            VALUES (?, ?)
        ''', (subject_id, hours))
    
    conn.commit()
    conn.close()

def update_completion_percentage(subject_id, percentage):
    """Update subject completion percentage"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id FROM progress WHERE subject_id = ?
    ''', (subject_id,))
    
    result = cursor.fetchone()
    
    if result:
        cursor.execute('''
            UPDATE progress 
            SET completion_percentage = ?, updated_at = CURRENT_TIMESTAMP
            WHERE subject_id = ?
        ''', (percentage, subject_id))
    else:
        cursor.execute('''
            INSERT INTO progress (subject_id, completion_percentage)
            VALUES (?, ?)
        ''', (subject_id, percentage))
    
    conn.commit()
    conn.close()

def update_revision_status(subject_id, status):
    """Update revision status for a subject"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE progress 
        SET revision_status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE subject_id = ?
    ''', (status, subject_id))
    
    conn.commit()
    conn.close()

def get_progress(subject_id):
    """Get progress data for a subject"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT hours_studied, completion_percentage, revision_status 
        FROM progress 
        WHERE subject_id = ?
    ''', (subject_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'hours_studied': result[0],
            'completion_percentage': result[1],
            'revision_status': result[2]
        }
    return None

def get_dashboard_stats():
    """Get overall dashboard statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total hours studied
    cursor.execute('SELECT COALESCE(SUM(hours_studied), 0) FROM progress')
    total_hours = cursor.fetchone()[0]
    
    # Average completion
    cursor.execute('SELECT COALESCE(AVG(completion_percentage), 0) FROM progress')
    avg_completion = cursor.fetchone()[0]
    
    # Number of subjects
    cursor.execute('SELECT COUNT(DISTINCT subject_id) FROM progress')
    num_subjects = cursor.fetchone()[0]
    
    # Recent activity
    cursor.execute('''
        SELECT s.name, p.updated_at 
        FROM progress p 
        JOIN subjects s ON p.subject_id = s.id 
        ORDER BY p.updated_at DESC 
        LIMIT 5
    ''')
    recent_activity = cursor.fetchall()
    
    conn.close()
    
    return {
        'total_hours': round(total_hours, 2),
        'avg_completion': round(avg_completion, 2),
        'num_subjects': num_subjects,
        'recent_activity': recent_activity
    }

def calculate_weekly_streak():
    """Calculate study streak (days studied in last 7 days)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    cursor.execute('''
        SELECT COUNT(DISTINCT DATE(updated_at)) 
        FROM progress 
        WHERE updated_at >= ?
    ''', (seven_days_ago,))
    
    streak = cursor.fetchone()[0]
    conn.close()
    
    return streak

def get_upcoming_deadlines():
    """Get upcoming exam deadlines"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT e.id, e.name, e.exam_date, s.name as subject
        FROM exams e
        JOIN subjects s ON e.subject_id = s.id
        WHERE e.exam_date >= DATE('now')
        ORDER BY e.exam_date ASC
        LIMIT 5
    ''')
    
    deadlines = cursor.fetchall()
    conn.close()
    
    return deadlines

def get_weak_topics(subject_id):
    """Identify weak topics based on mock test performance"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT test_type, AVG(CAST(obtained_marks AS FLOAT) / total_marks * 100) as avg_score
        FROM mock_tests
        WHERE subject_id = ?
        GROUP BY test_type
        ORDER BY avg_score ASC
    ''', (subject_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    weak_topics = []
    for test_type, avg_score in results:
        if avg_score < 60:
            weak_topics.append({
                'topic': test_type,
                'score': round(avg_score, 2),
                'status': 'Weak'
            })
    
    return weak_topics
