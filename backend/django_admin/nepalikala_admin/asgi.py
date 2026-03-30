"""
ASGI config for nepalikala_admin project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nepalikala_admin.settings')

application = get_asgi_application()
