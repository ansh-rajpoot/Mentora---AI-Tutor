# Mentora - Deployment Guide

## Quick Setup Options

### Option 1: ngrok (INSTANT - Best for Testing)
**Use this to quickly share your app online**

#### Step 1: Start Django Server
```bash
cd c:\Users\Hamza\OneDrive\Documents\GitHub\Mentora---AI-Tutor
python manage.py runserver 0.0.0.0:8000
```

#### Step 2: Open Another Terminal and Run ngrok
```bash
cd c:\Users\Hamza\OneDrive\Documents\GitHub\Mentora---AI-Tutor
.\ngrok.exe http 8000
```

#### Step 3: Share Your Public URL
ngrok will show a URL like:
```
https://abc123def456.ngrok.io
```

**Share this URL with anyone to access your site!**

**Duration:** Free plan = 2 hours per session
**Note:** You need to keep both terminals running

---

### Option 2: PythonAnywhere (BEST - Permanent Solution)
**Use this for a permanent online presence with a subdomain**

#### Setup Instructions:

1. **Sign up** at https://www.pythonanywhere.com (Free account available)

2. **Upload Your Project**
   - Go to Files → Upload
   - Upload your entire project folder

3. **Create a Web App**
   - Web → Add a new web app
   - Python 3.10
   - Django

4. **Configure Django App**
   - Edit the WSGI file to point to your project
   - Set source code location to your uploaded project

5. **Add to ALLOWED_HOSTS**
   Your subdomain will be: `yourusername.pythonanywhere.com`
   - Add this to `ALLOWED_HOSTS` in `settings.py`
   - Example: `ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'localhost']`

6. **Reload Web App**
   - Click "Reload" on the Web tab

7. **Your Site is Live!**
   Access it at: https://yourusername.pythonanywhere.com

---

## Environment Variables (For Production)

For PythonAnywhere, create a `.env` file with:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourusername.pythonanywhere.com
```

Then update `settings.py` to load from `.env`:
```python
from dotenv import load_dotenv
load_dotenv()

DEBUG = os.getenv('DEBUG', 'True') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-...')
```

---

## Database Migration for PythonAnywhere

After uploading to PythonAnywhere:
```bash
python manage.py migrate
```

---

## Static Files for PythonAnywhere

PythonAnywhere requires static files collection:
```bash
python manage.py collectstatic --noinput
```

Then configure in PythonAnywhere:
- Static files URL: `/static/`
- Directory: `/home/yourusername/your-project-path/staticfiles/`

---

## Troubleshooting

### ngrok Issues
- **"Port already in use"**: Kill other processes on port 8000
- **"Failed to connect"**: Make sure Django server is running
- **URL keeps changing**: Paid ngrok plan keeps same URL

### PythonAnywhere Issues
- **Import errors**: Check Python version matches (3.8+)
- **Database not found**: Run migrations on PythonAnywhere
- **Static files not showing**: Run collectstatic command
- **Module not found**: Install packages in PythonAnywhere console

---

## Current Configuration

Your app is configured to support:
- ✓ Local development (localhost:8000)
- ✓ ngrok tunneling (*.ngrok.io)
- ✓ PythonAnywhere (*.pythonanywhere.com)
- ✓ Custom domains (when configured)

---

## Quick Commands Reference

**Start Django:**
```bash
python manage.py runserver
```

**Start with ngrok:**
```bash
# Terminal 1:
python manage.py runserver 0.0.0.0:8000

# Terminal 2:
.\ngrok.exe http 8000
```

**Prepare for PythonAnywhere:**
```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

---

**Questions?** Check the Django deployment documentation at:
https://docs.djangoproject.com/en/stable/howto/deployment/
