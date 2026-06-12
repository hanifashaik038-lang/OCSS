# OCSS - Setup Guide

## Detailed Installation & Configuration Guide

### System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB for application + space for uploads

### Step-by-Step Installation

#### 1. Download & Navigate to Project

```bash
# Extract the OCSS folder if downloaded as zip
cd path/to/OCSS
```

#### 2. Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages:
- streamlit (web framework)
- pandas (data manipulation)
- plotly (visualization)
- python-pptx (PowerPoint handling)
- python-docx (Word document handling)
- PyPDF2 (PDF handling)
- pillow (image handling)
- openai (AI features)
- requests (HTTP requests)

#### 4. Initialize Database

```bash
python database/db_init.py
```

This creates the SQLite database with all necessary tables.

#### 5. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Configuration

#### Streamlit Config
Edit `.streamlit/config.toml`:
- Customize theme colors
- Adjust font settings
- Configure server port
- Set logging level

#### Environment Variables
Create `.env` file for API keys:
```
OPENAI_API_KEY=sk-your-key-here
```

### Troubleshooting

#### Issue: "Module not found" errors
**Solution**: 
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt` again

#### Issue: Port 8501 already in use
**Solution**:
```bash
streamlit run app.py --server.port 8502
```

#### Issue: Database errors
**Solution**:
- Delete `database/app.db`
- Run: `python database/db_init.py`
- Restart the application

#### Issue: File upload not working
**Solution**:
- Ensure `uploads/` folder exists
- Check file permissions
- Restart Streamlit

### Production Deployment

#### Using Streamlit Cloud
1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Select your repository
4. Deploy

#### Using Docker
1. Create Dockerfile:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

2. Build and run:
```bash
docker build -t ocss .
docker run -p 8501:8501 ocss
```

### Backup & Data Management

#### Backing Up Data
```bash
# Backup database
cp database/app.db database/app.db.backup

# Backup uploads
cp -r uploads/ uploads.backup/
```

#### Restoring Data
```bash
# Restore database
cp database/app.db.backup database/app.db

# Restore uploads
cp -r uploads.backup/ uploads/
```

### Performance Optimization

- **Clear cache**: Delete `.streamlit/` folder and rerun
- **Database maintenance**: Periodically clean old test data
- **File cleanup**: Archive old uploads to external storage
- **Memory optimization**: Limit concurrent uploads to <100MB each

### Security Best Practices

1. **API Keys**: Never commit `.env` to version control
2. **Database**: Backup regularly to prevent data loss
3. **File Upload**: Only allow trusted file types
4. **Authentication**: Implement user login for production
5. **HTTPS**: Use HTTPS in production environments

### Support Resources

- Streamlit Documentation: https://docs.streamlit.io
- Python Documentation: https://docs.python.org
- SQLite Documentation: https://www.sqlite.org/docs.html
- GitHub Issues: Check project repository for known issues
