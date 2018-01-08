"""
Django settings for relops_hardware_controller project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

from configurations import Configuration, values


class Base(Configuration):

    SECRET_KEY = values.SecretValue()

    # Password validation
    # https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Internationalization
    # https://docs.djangoproject.com/en/1.10/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.10/howto/static-files/
    STATIC_URL = '/static/'

    CONN_MAX_AGE = values.IntegerValue(60)

    ALLOWED_HOSTS = values.ListValue([])

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.staticfiles',

        'relops_hardware_controller.apps.RelopsHardwareControllerAppConfig',
        'relops_hardware_controller.api',

        'django_celery_results',
        'rest_framework',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    REDIS_URL = values.Value('redis://redis:6379/0')

    # Use redis as the Celery broker.
    @property
    def CELERY_BROKER_URL(self):
        return self.REDIS_URL

    @property
    def CACHES(self):
        return {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': self.REDIS_URL,
                'OPTIONS': {
                    'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',  # noqa
                    'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',  # noqa
                },
            },
        }

    ROOT_URLCONF = 'relops_hardware_controller.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'relops_hardware_controller.wsgi.application'

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'ugrryo)w9y0(*i^-zjq+%)=o^g*-0l%l*7!5qzrg3j$y3mtp*$'

    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'

    # The django_celery_results backend.
    CELERY_RESULT_BACKEND = 'django-cache'

    # Throw away task results after 1 hour, for debugging purposes.
    # CELERY_RESULT_EXPIRES = datetime.timedelta(minutes=60)

    # Track if a task has been started, not only pending etc.
    CELERY_TASK_TRACK_STARTED = True

    # Add a 5 minute soft timeout to all Celery tasks.
    CELERY_TASK_SOFT_TIME_LIMIT = 60 * 5

    # And a 10 minute hard timeout.
    CELERY_TASK_TIME_LIMIT = CELERY_TASK_SOFT_TIME_LIMIT * 2

    BUGZILLA_URL = values.URLValue()
    BUGZILLA_API_KEY = values.SecretValue()

    XEN_URL = values.URLValue()
    XEN_USERNAME = values.Value()
    XEN_PASSWORD = values.SecretValue()

    ILO_USERNAME = values.Value()
    ILO_PASSWORD = values.SecretValue()

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'UNAUTHENTICATED_USER': 'relops_hardware_controller.api.models.TaskclusterUser',
    }

    TASK_NAMES = [
        # 'loan',
        'reboot',
        # 'reimage',
        # 'return_loan',
    ]

    CORS_ORIGIN = values.Value()

    TASKCLUSTER_CLIENT_ID = values.Value('', environ_prefix=None)
    TASKCLUSTER_ACCESS_TOKEN = values.SecretValue(environ_prefix=None)

    REQUIRED_TASKCLUSTER_SCOPE_SETS = [
        ['project:relops-hardware-controller:{}'.format(task_name)]
        for task_name in TASK_NAMES
    ]

    # Path to JSON file mapping FDQNs to PDUs with format:
    # {
    #   "t-yosemite-r7-0001.test.releng.scl3.mozilla.com": {
    #     "ssh": {
    #       "user": "reboot-forcecommand-user",
    #       "key_file": "~/.ssh/test_ipmitool_pass.key",
    #      }
    #    },
    #   ...
    # }
    FQDN_TO_SSH_FILE = values.PathValue('ssh.json')

    # Path to JSON file mapping FDQNs to PDUs with format:
    # {
    #   "t-yosemite-r7-0001.test.releng.scl3.mozilla.com": {
    #     "ipmi": {
    #       "user": "test_reboot_user",
    #       "password": "test_ipmitool_pass"
    #     }
    #   },
    #   ...
    # }
    FQDN_TO_IPMI_FILE = values.PathValue('ipmi.json')

    # Path to JSON file mapping FDQNs to PDUs with format:
    # {
    #   "t-yosemite-r7-0001.test.releng.scl3.mozilla.com": {
    #     "pdu": "pdu1.r201-6.ops.releng.scl3.mozilla.com:AA1"
    #    },
    #   ...
    # }
    FQDN_TO_PDU_FILE = values.PathValue('pdus.json')

    # Path to JSON file mapping FDQNs to PDUs with format:
    # {
    #   "t-yosemite-r7-0001.test.releng.scl3.mozilla.com": {
    #     "xen_uuid": "pdu1.r201-6.ops.releng.scl3.mozilla.com:AA1"
    #    },
    #   ...
    # }
    FQDN_TO_XEN_FILE = values.PathValue('xen.json')

    # how many seconds to wait for a machine to go down and come back up
    DOWN_TIMEOUT = values.IntegerValue(60)
    UP_TIMEOUT = values.IntegerValue(300)

    REBOOT_METHODS = [
        'ssh_reboot',
        'ipmi_reboot',  # ipmi pdu for iX hardware (linux, xp, w8, w10)
        'snmp_reboot',  # snmp pdu for mac minis
        'xen_reboot',  # for moonshot HW
        'ilo_reboot',  # for moonshot HW
        'file_bugzilla_bug',  # give up and file a bug
    ]


class Dev(Base):
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    CORS_ORIGIN = 'localhost'

    BUGZILLA_URL = 'https://landfill.bugzilla.org/bugzilla-5.0-branch/rest/'

    XEN_URL = 'https://xenapiserver/'
    XEN_USERNAME = 'xen_dev_username'

    ILO_USERNAME = 'ilo_dev_username'

    TASKCLUSTER_CLIENT_ID = 'test-tc-client-id'
    TASKCLUSTER_ACCESS_TOKEN = values.Value('test-tc-access-token')

    TASK_NAMES = [
        'ping',
    ]

    REQUIRED_TASKCLUSTER_SCOPE_SETS = [
        ['project:relops-hardware-controller:{}'.format(task_name)]
        for task_name in TASK_NAMES
    ]


class Prod(Base):
    ALLOWED_HOSTS = ['tools.taskcluster.net']
    CORS_ORIGIN = 'tools.taskcluster.net'


class Test(Base):
    DEBUG = False

    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    CORS_ORIGIN = 'localhost'

    SECRET_KEY = values.Value('not-so-secret-after-all')

    BUGZILLA_URL = 'https://landfill.bugzilla.org/bugzilla-5.0-branch/rest/'
    BUGZILLA_API_KEY = values.Value('not-so-secret-after-all')

    XEN_URL = 'https://xenapiserver/'
    XEN_USERNAME = 'xen_dev_username'
    XEN_PASSWORD = values.Value('not-so-secret-after-all')

    ILO_USERNAME = 'ilo_dev_username'
    ILO_PASSWORD = values.Value('not-so-secret-ilo-pass-after-all')

    TASKCLUSTER_CLIENT_ID = 'test-tc-client-id'
    TASKCLUSTER_ACCESS_TOKEN = values.Value('test-tc-access-token')

    TASK_NAMES = [
        'ping',
    ]

    REQUIRED_TASKCLUSTER_SCOPE_SETS = [
        ['project:relops-hardware-controller:{}'.format(task_name)]
        for task_name in TASK_NAMES
    ]
