"""
Tests for the SqlGrader.submit_query JSON handler
"""

import json
from unittest import TestCase
from unittest.mock import Mock, patch

from opaque_keys.edx.locator import CourseLocator
from webob import Request
from xblock.field_data import DictFieldData

from sql_grader.xblocks import SqlGrader


def make_an_xblock(**kwargs):
    """Create a SqlGrader XBlock instance for testing."""
    course_id = CourseLocator("foo", "bar", "baz")
    runtime = Mock(
        course_id=course_id,
        service=Mock(return_value=Mock(_catalog={})),
    )
    scope_ids = Mock()
    field_data = DictFieldData(kwargs)
    xblock = SqlGrader(runtime, field_data, scope_ids)
    xblock.xmodule_runtime = runtime
    return xblock


def make_request(body_dict):
    """Create a webob Request with JSON body, as XBlock.json_handler expects."""
    request = Request.blank("/")
    request.method = "POST"
    request.content_type = "application/json"
    request.body = json.dumps(body_dict).encode("utf-8")
    return request


class TestSubmitQuery(TestCase):
    """Test the submit_query JSON handler on SqlGrader."""

    def setUp(self):
        self.xblock = make_an_xblock(
            dataset="rating",
            answer_query="SELECT * FROM Movie",
            verify_query="",
            modification_query="",
            is_ordered=False,
            weight=1,
        )

    @patch("sql_grader.mixins.grading.attempt_safe")
    def test_correct_submission_returns_comparison_true(self, mock_attempt):
        """A correct query should produce comparison=True in the response."""
        mock_attempt.return_value = (
            [(101, "Gone with the Wind", 1939, "Victor Fleming")],
            [(101, "Gone with the Wind", 1939, "Victor Fleming")],
            None,
            True,
        )
        response = self.xblock.submit_query(make_request({"query": "SELECT * FROM Movie"}))
        result = json.loads(response.body)
        self.assertTrue(result["comparison"])
        self.assertIsNone(result["error"])

    @patch("sql_grader.mixins.grading.attempt_safe")
    def test_wrong_submission_returns_comparison_false(self, mock_attempt):
        """An incorrect query should produce comparison=False."""
        mock_attempt.return_value = (
            [(101,)],
            [(101, "Gone with the Wind", 1939, "Victor Fleming")],
            None,
            False,
        )
        response = self.xblock.submit_query(make_request({"query": "SELECT mID FROM Movie"}))
        result = json.loads(response.body)
        self.assertFalse(result["comparison"])

    @patch("sql_grader.mixins.grading.attempt_safe")
    def test_stores_raw_response(self, mock_attempt):
        """The submitted query text should be stored in raw_response (stripped)."""
        mock_attempt.return_value = ([], [], None, False)
        self.xblock.submit_query(make_request({"query": "  SELECT 1  "}))
        self.assertEqual(self.xblock.raw_response, "SELECT 1")

    @patch("sql_grader.mixins.grading.attempt_safe")
    def test_empty_query(self, mock_attempt):
        """An empty query submission should still be processed."""
        mock_attempt.return_value = (None, None, "syntax error", False)
        self.xblock.submit_query(make_request({"query": ""}))
        self.assertEqual(self.xblock.raw_response, "")

    @patch("sql_grader.mixins.grading.attempt_safe")
    def test_missing_query_key_defaults_to_empty(self, mock_attempt):
        """If 'query' key is missing from data, it defaults to empty string."""
        mock_attempt.return_value = (None, None, "error", False)
        self.xblock.submit_query(make_request({}))
        self.assertEqual(self.xblock.raw_response, "")

    @patch("sql_grader.mixins.grading.attempt_safe")
    def test_response_includes_verify_and_modification(self, mock_attempt):
        """
        The response should include verify_query and modification_query
        so the frontend can display problem context.
        """
        xblock = make_an_xblock(
            dataset="rating",
            answer_query="INSERT INTO Movie VALUES(1,'T',2000,'D')",
            verify_query="SELECT * FROM Movie WHERE mID=1",
            modification_query="DELETE FROM Movie WHERE mID > 200",
            is_ordered=False,
        )
        mock_attempt.return_value = ([(1, "T", 2000, "D")], [(1, "T", 2000, "D")], None, True)
        response = xblock.submit_query(make_request({"query": "INSERT INTO Movie VALUES(1,'T',2000,'D')"}))
        result = json.loads(response.body)
        self.assertEqual(result["verify"], "SELECT * FROM Movie WHERE mID=1")
        self.assertEqual(result["modification"], "DELETE FROM Movie WHERE mID > 200")

    @patch("sql_grader.mixins.grading.attempt_safe")
    def test_error_in_query_returned_to_frontend(self, mock_attempt):
        """SQL errors should be forwarded to the frontend in the response."""
        mock_attempt.return_value = (None, None, "no such table: Foo", False)
        response = self.xblock.submit_query(make_request({"query": "SELECT * FROM Foo"}))
        result = json.loads(response.body)
        self.assertEqual(result["error"], "no such table: Foo")
        self.assertIsNone(result["result"])
        self.assertIsNone(result["expected"])

    @patch("sql_grader.mixins.grading.attempt_safe")
    def test_score_published_on_submission(self, mock_attempt):
        """submit_query should publish the grade via the runtime."""
        mock_attempt.return_value = ([], [], None, True)
        self.xblock.submit_query(make_request({"query": "SELECT 1"}))
        self.xblock.runtime.publish.assert_called()
