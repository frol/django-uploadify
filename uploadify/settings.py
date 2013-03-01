from django.conf import settings
STATIC_URL = getattr(settings, 'STATIC_URL', '')
MEDIA_URL = getattr(settings, 'MEDIA_URL', '')

# Uploadify root folder path, relative to STATIC_URL
UPLOADIFY_PATH = getattr(settings, 'UPLOADIFY_PATH', 
    '%s%s' % (STATIC_URL, 'js/uploadify/'))

# Upload path that files are sent to
UPLOADIFY_UPLOAD_PATH = getattr(settings, 'UPLOADIFY_UPLOAD_PATH', 
    '%s%s' % (MEDIA_URL, 'uploads/'))

# Version of uploadify that you use. Available versions are 2 or 3
UPLOADIFY_VERSION = getattr(settings, 'UPLOADIFY_VERSION', 3)
