
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER':'',
        'PASSWORD':'',
        'HOST':'localhost',
        'PORT': 5432,
    }
}