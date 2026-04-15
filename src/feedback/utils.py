"""Utilities for feedback app"""

import sys
from urllib.parse import urlencode, urlparse, urlunparse

from django.conf import settings
from opaque_keys.edx.keys import UsageKey


def _(text):
    """Dummy `gettext` replacement to make string extraction tools scrape strings marked for translation"""
    return text


def get_lms_link_for_item(location, preview=False):
    """
    Returns an LMS link to the course with a jump_to to the provided location.
    """
    assert isinstance(location, UsageKey)

    # Hack: Import SiteConfiguration from openedx-platform.
    # Please note that XBlocks should not import core openedx-platform code. Do not
    # replicate this pattern elsewhere. If you need information from the platform, it's better
    # to catch an event, hook into a filter, or define and use an XBlock runtime service.
    try:
        # pylint: disable=import-outside-toplevel
        from openedx.core.djangoapps.site_configuration.models import SiteConfiguration
    except ImportError:
        if "unittest" in sys.modules.keys():
            # Fail silently when testing. We can't install openedx-platform for tests.
            return None
        # Otherwise, fail loudly, so that we will notice if the openedx-platform import path changes.
        raise

    lms_base = SiteConfiguration.get_value_for_org(location.org, "LMS_ROOT_URL", settings.LMS_ROOT_URL)

    if lms_base is None:
        return None

    query_string = ""
    if preview:
        query_string = urlencode({"preview": "1"})

    url_parts = list(urlparse(lms_base))
    url_parts[2] = f"/courses/{location.course_key}/jump_to/{location}"
    url_parts[4] = query_string

    return urlunparse(url_parts)
