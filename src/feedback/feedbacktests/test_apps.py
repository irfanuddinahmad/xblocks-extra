"""Tests for the feedback app's Open edX plugin configuration."""

from importlib import import_module

import pytest

from feedback.apps import FeedbackConfig

SETTINGS_CONFIG = FeedbackConfig.plugin_app["settings_config"]

DECLARED_SETTINGS = [
    (project_type, settings_type, config["relative_path"])
    for project_type, by_settings_type in SETTINGS_CONFIG.items()
    for settings_type, config in by_settings_type.items()
]


@pytest.mark.parametrize("project_type,settings_type,relative_path", DECLARED_SETTINGS)
def test_declared_plugin_settings_exist(project_type, settings_type, relative_path):
    """
    Every settings module the plugin declares must import and define ``plugin_settings``.

    The platform's ``add_plugins`` imports each declared module for the matching settings
    type, so a missing module breaks LMS/CMS startup with those settings.
    """
    module = import_module(f"{FeedbackConfig.name}.{relative_path}")
    assert callable(getattr(module, "plugin_settings", None)), (project_type, settings_type)
