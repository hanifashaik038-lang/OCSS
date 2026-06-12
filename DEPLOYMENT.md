# OCSS - Deployment Guide

## Local Deployment

### Prerequisites
- Python 3.8+
- Git (optional, for version control)

### Quick Setup
```bash
# 1. Navigate to project
cd OCSS

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python database/db_init.py

# 5. Run application
streamlit run app.py
```

Access at: http://localhost:8501

---

## Streamlit Cloud Deployment

### Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial OCSS commit"
   git push origin main
   ```

2. **Connect to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Sign up with GitHub account
   - Click "New app"
   - Select your repository and branch
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Configure Secrets** (in Streamlit Cloud)
   - Go to app settings
   - Add secrets:
     ```
     OPENAI_API_KEY = "sk-..."
     ```

### Limits
- Free tier: 1 app, 1GB storage
- Maximum runtime: 24 hours
- Respects resource limits

---

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create data directories
RUN mkdir -p database uploads data assets

# Initialize database
RUN python database/db_init.py

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run Locally

```bash
# Build image
docker build -t ocss:latest .

# Run container
docker run -p 8501:8501 \
  -v $(pwd)/database:/app/database \
  -v $(pwd)/uploads:/app/uploads \
  ocss:latest
```

### Push to Docker Hub

```bash
# Tag image
docker tag ocss:latest yourusername/ocss:latest

# Push to Docker Hub
docker push yourusername/ocss:latest
```

---

## AWS Deployment

### Option 1: AWS Elastic Beanstalk

1. **Prepare application**
   ```bash
   # Create .ebextensions directory
   mkdir .ebextensions
   ```

2. **Create configuration file** (`.ebextensions/python.config`)
   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: app:app
   commands:
     01_install_deps:
       command: "pip install -r requirements.txt"
     02_init_db:
       command: "python database/db_init.py"
   ```

3. **Deploy**
   ```bash
   eb init -p python-3.9 ocss
   eb create ocss-env
   eb deploy
   ```

### Option 2: AWS EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 20.04 LTS
   - Instance type: t3.small (minimum)
   - Security group: Allow ports 80, 443, 8501

2. **SSH and Setup**
   ```bash
   # Connect to instance
   ssh -i key.pem ubuntu@your-instance-ip
   
   # Install Python and dependencies
   sudo apt-get update
   sudo apt-get install -y python3.9 python3-pip git
   
   # Clone repository
   git clone your-repo-url
   cd OCSS
   
   # Install requirements
   pip3 install -r requirements.txt
   
   # Initialize database
   python3 database/db_init.py
   
   # Run with nohup (background)
   nohup streamlit run app.py --server.port 8501 &
   ```

3. **Setup Reverse Proxy with Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

---

## Heroku Deployment

### 1. Create Procfile
```
web: streamlit run app.py --server.port=$PORT
```

### 2. Create runtime.txt
```
python-3.9.16
```

### 3. Deploy
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-...

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

---

## Google Cloud Run Deployment

### 1. Create Dockerfile (same as Docker section)

### 2. Configure gcloud
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 3. Build and Push
```bash
# Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ocss

# Deploy
gcloud run deploy ocss \
  --image gcr.io/YOUR_PROJECT_ID/ocss \
  --platform managed \
  --region us-central1 \
  --memory 1Gi \
  --timeout 3600
```

---

## DigitalOcean App Platform

### 1. Create app.yaml
```yaml
name: ocss
services:
- name: ocss
  github:
    repo: your-username/ocss
    branch: main
  build_command: pip install -r requirements.txt && python database/db_init.py
  run_command: streamlit run app.py --server.port 8080
  http_port: 8080
  health_check:
    http_path: /_stcore/health
```

### 2. Deploy
- Push code to GitHub
- Connect repository in DigitalOcean App Platform
- Deploy automatically

---

## Performance Optimization

### For Production
1. **Enable caching**
   ```python
   @st.cache_data
   def expensive_query():
       # ...
   ```

2. **Use CDN for static files**
   - CloudFront (AWS)
   - CloudFlare
   - Netlify

3. **Database optimization**
   - Add indexes on frequently queried columns
   - Archive old data
   - Regular backups

4. **Monitoring**
   - Set up application monitoring
   - Track performance metrics
   - Monitor error rates

### Recommended Specs
- **Minimum**: 1GB RAM, 1 CPU, 10GB storage
- **Recommended**: 2GB RAM, 2 CPU, 20GB storage
- **High Traffic**: 4GB+ RAM, 4+ CPU, 50GB+ storage

---

## Backup and Recovery

### Automated Backups
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backup/ocss"
mkdir -p $BACKUP_DIR

# Backup database
cp database/app.db $BACKUP_DIR/app.db.$(date +%Y%m%d_%H%M%S)

# Backup uploads (keep last 30 days)
find $BACKUP_DIR -name "app.db.*" -mtime +30 -delete
```

### Cloud Backup
- AWS S3
- Google Cloud Storage
- DigitalOcean Spaces

---

## Monitoring & Logging

### Application Monitoring
- Streamlit includes built-in metrics
- Access via browser developer tools

### External Monitoring
- Sentry (error tracking)
- DataDog (infrastructure monitoring)
- New Relic (APM)

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Application started")
logger.error("Error message", exc_info=True)
```

---

## Troubleshooting

### Common Issues

**Issue**: App times out during initialization
- **Solution**: Increase timeout in cloud platform settings

**Issue**: Database locked error
- **Solution**: Check for concurrent access, use WAL mode

**Issue**: File upload fails
- **Solution**: Check storage permissions and disk space

**Issue**: High memory usage
- **Solution**: Implement pagination, reduce cache size

---

## Security Checklist

- [ ] API keys stored in environment variables only
- [ ] Database backups encrypted
- [ ] HTTPS enabled for all connections
- [ ] File uploads validated
- [ ] SQL injection prevention (use parameterized queries)
- [ ] CORS configured properly
- [ ] Rate limiting enabled
- [ ] User authentication implemented (for production)
