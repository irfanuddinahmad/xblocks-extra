"""
Shared Django test settings for the xblocks-extra repository.

All XBlocks in this repo share these settings during test runs.
Add any new XBlock app to INSTALLED_APPS below when migrating it in.
"""

from workbench.settings import *  # pylint: disable=wildcard-import  # noqa: F403, I001
from django.conf.global_settings import LOGGING  # noqa: F401

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "feedback",
    "freetextresponse",
    "workbench",
]

FEATURES = {
    "ENABLE_FEEDBACK_INSTRUCTOR_VIEW": True,
}

SECRET_KEY = "fake-key"

LMS_ROOT_URL = "https://example.com"
