"""
WSGI config for guarani_app project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guarani_app.settings')

application = get_wsgi_application()

# Vercel serverless function handler
app = application
