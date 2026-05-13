"""
Settings for freetextresponse xblock
"""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    },
}
LOCALE_PATHS = [
    "freetextresponse/conf/locale",
]
SECRET_KEY = "freetextresponse_SECRET_KEY"
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
