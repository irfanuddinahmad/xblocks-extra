"""
Extend XBlock with additional user functionality
"""


# pylint: disable=too-few-public-methods
class MissingDataFetcherMixin:
    """
    The mixin used for getting the student_id of the current user.
    """

    def get_student_id(self):
        """
        Get the student id.
        """
        if hasattr(self, "xmodule_runtime"):
            student_id = self.xmodule_runtime.anonymous_student_id
            # pylint:disable=E1101
        else:
            student_id = str(self.scope_ids.user_id or "")
        return student_id
