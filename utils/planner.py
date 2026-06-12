from datetime import datetime, timedelta
import sqlite3
from database.db_init import get_connection

def add_task(subject_id, title, description, due_date, priority='Medium'):
    """Add a new task to the planner"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO planner_tasks 
        (subject_id, title, description, due_date, priority)
        VALUES (?, ?, ?, ?, ?)
    ''', (subject_id, title, description, due_date, priority))
    
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def get_tasks(subject_id=None):
    """Get all tasks, optionally filtered by subject"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if subject_id:
        cursor.execute('''
            SELECT * FROM planner_tasks 
            WHERE subject_id = ? 
            ORDER BY due_date ASC
        ''', (subject_id,))
    else:
        cursor.execute('''
            SELECT * FROM planner_tasks 
            ORDER BY due_date ASC
        ''')
    
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def mark_task_complete(task_id):
    """Mark a task as complete"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE planner_tasks 
        SET completed = 1 
        WHERE id = ?
    ''', (task_id,))
    
    conn.commit()
    conn.close()

def update_task(task_id, title, description, due_date, priority):
    """Update an existing task"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE planner_tasks 
        SET title = ?, description = ?, due_date = ?, priority = ?
        WHERE id = ?
    ''', (title, description, due_date, priority, task_id))
    
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Delete a task"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM planner_tasks WHERE id = ?', (task_id,))
    
    conn.commit()
    conn.close()

def get_upcoming_tasks(days=7):
    """Get tasks due within the next N days"""
    conn = get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().date()
    future_date = today + timedelta(days=days)
    
    cursor.execute('''
        SELECT * FROM planner_tasks 
        WHERE due_date BETWEEN ? AND ? 
        AND completed = 0
        ORDER BY due_date ASC
    ''', (str(today), str(future_date)))
    
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def generate_revision_schedule(exam_date, subject_id, num_sessions=10):
    """Generate a revision schedule for an exam"""
    exam = datetime.strptime(exam_date, '%Y-%m-%d').date()
    today = datetime.now().date()
    days_available = (exam - today).days
    
    schedule = []
    if days_available > 0:
        interval = days_available // num_sessions
        
        for i in range(num_sessions):
            revision_date = today + timedelta(days=interval * (i + 1))
            task_id = add_task(
                subject_id=subject_id,
                title=f"Revision Session {i+1}",
                description=f"Complete revision session {i+1} for exam",
                due_date=str(revision_date),
                priority='High'
            )
            schedule.append({
                'session': i + 1,
                'date': str(revision_date),
                'task_id': task_id
            })
    
    return schedule
