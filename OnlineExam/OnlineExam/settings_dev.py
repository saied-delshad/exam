
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'examination',
        'USER':'examiner',
        'PASSWORD':'Aliz12363',
        'HOST':'localhost',
        'PORT': 5432,
    }
}