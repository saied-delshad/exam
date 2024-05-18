
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['*', 'meraj.exama.ir']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'exam_db',
        # 'NAME': 'back_up',
        'USER': 'examiner',
        'PASSWORD': 'Aliz12363',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR , 'static'),
    os.path.join(BASE_DIR, 'frontend/dist')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
