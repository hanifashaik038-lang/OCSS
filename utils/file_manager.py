import os
import shutil
from pathlib import Path
import mimetypes

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'.pdf', '.pptx', '.docx', '.png', '.jpg', '.jpeg', '.gif'}

def create_subject_folder(subject_name, semester_name):
    """Create a folder for a subject under semester"""
    semester_dir = os.path.join(UPLOADS_DIR, semester_name)
    subject_dir = os.path.join(semester_dir, subject_name)
    
    os.makedirs(subject_dir, exist_ok=True)
    return subject_dir

def save_uploaded_file(uploaded_file, subject_folder):
    """Save an uploaded file to the subject folder"""
    if not uploaded_file:
        return None
    
    os.makedirs(subject_folder, exist_ok=True)
    file_path = os.path.join(subject_folder, uploaded_file.name)
    
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def get_file_extension(filename):
    """Get file extension"""
    return os.path.splitext(filename)[1].lower()

def is_allowed_file(filename):
    """Check if file type is allowed"""
    return get_file_extension(filename) in ALLOWED_EXTENSIONS

def get_files_in_folder(folder_path):
    """Get list of files in a folder"""
    if not os.path.exists(folder_path):
        return []
    
    files = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            files.append({
                'name': filename,
                'path': filepath,
                'size': os.path.getsize(filepath),
                'type': get_file_extension(filename)
            })
    return files

def delete_file(file_path):
    """Delete a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"Error deleting file: {e}")
    return False

def get_file_size_mb(file_path):
    """Get file size in MB"""
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / (1024 * 1024)
    return 0
