"""
Common Test settings for eox_hooks project.
For more information on this file, see
https://docs.djangoproject.com/en/2.22/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.22/ref/settings/
"""

from workbench.settings import *  # noqa: F403  # pylint: disable=wildcard-import

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "feedback",
    "workbench",
]

FEATURES = {
    "ENABLE_FEEDBACK_INSTRUCTOR_VIEW": True,
}

SECRET_KEY = "fake-key"
