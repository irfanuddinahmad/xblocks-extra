"""
A SQL database graded component

Implemented in SQLite
"""

try:
    from .xblocks import SqlGrader as SqlGrader
except Exception:  # noqa: BLE001
    # In the codejail sandbox Django is not configured, so XBlock field
    # defaults (which use gettext_lazy) fail at import time.  The sandbox
    # only needs sql_grader.problem — this is safe to swallow.
    pass
