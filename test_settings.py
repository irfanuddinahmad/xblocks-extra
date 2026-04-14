"""
Common test settings for xblocks-extra.

"""

from workbench.settings import *  # pylint: disable=wildcard-import  # noqa: F403
from django.conf.global_settings import LOGGING  # noqa: F401

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "feedback",
    "workbench",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

FEATURES = {
    "ENABLE_FEEDBACK_INSTRUCTOR_VIEW": True,
}

SECRET_KEY = "fake-key"
USE_TZ = True
