DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     'hc',
        'USER':     'postgres',
        #'PASSWORD': 'your-database-password-here',
        'TEST': {'CHARSET': 'UTF8'}
    }
}

DEBUG = True