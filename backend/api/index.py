import os
import django
from django.core.wsgi import get_wsgi_application
from vercel_wsgi import handle_wsgi

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendApi.settings')

# Initialize Django
django.setup()

# Get the WSGI application
app = get_wsgi_application()

# Vercel handler
def handler(event, context):
    return handle_wsgi(app, event, context)