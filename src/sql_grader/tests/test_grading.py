"""
Tests for the grading mixins: attempt_safe, Scorable, and XBlockDataMixin
"""

from unittest import TestCase
from unittest.mock import Mock, patch

from opaque_keys.edx.locator import CourseLocator
from xblock.field_data import DictFieldData
from xblock.scorable import Score

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


class TestAttemptSafe(TestCase):
    """Test the attempt_safe function that sandboxes SQL execution via codejail."""

    @patch("sql_grader.mixins.grading.safe_exec")
    def test_successful_execution(self, mock_safe_exec):
        """
        When codejail executes successfully, attempt_safe returns the
        results dict populated by the sandboxed code.
        """
        from sql_grader.mixins.grading import attempt_safe

        def side_effect(code, results, **kwargs):
            results["submission_result"] = [(1, "Test")]
            results["answer_result"] = [(1, "Test")]
            results["error"] = None
            results["comparison"] = True

        mock_safe_exec.side_effect = side_effect

        submission, answer, error, comparison = attempt_safe(
            dataset="rating",
            answer_query="SELECT 1",
            verify_query=None,
            modification_query=None,
            is_ordered=True,
            query="SELECT 1",
        )
        self.assertEqual(submission, [(1, "Test")])
        self.assertEqual(answer, [(1, "Test")])
        self.assertIsNone(error)
        self.assertTrue(comparison)
        mock_safe_exec.assert_called_once()

    @patch("sql_grader.mixins.grading.safe_exec")
    def test_codejail_exception_returns_safe_error(self, mock_safe_exec):
        """
        When codejail raises SafeExecException (e.g., resource limits),
        attempt_safe should return a user-friendly error message.
        """
        from codejail.safe_exec import SafeExecException

        from sql_grader.mixins.grading import attempt_safe

        mock_safe_exec.side_effect = SafeExecException("timeout")

        submission, answer, error, comparison = attempt_safe(
            dataset="rating",
            answer_query="SELECT 1",
            verify_query=None,
            modification_query=None,
            is_ordered=True,
            query="SELECT 1",
        )
        self.assertIsNone(submission)
        self.assertIsNone(answer)
        self.assertIsNotNone(error)
        self.assertIsNone(comparison)

    @patch("sql_grader.mixins.grading.safe_exec")
    def test_passes_correct_parameters_to_sandbox(self, mock_safe_exec):
        """Verify the globals dict passed to safe_exec contains all problem parameters."""
        from sql_grader.mixins.grading import attempt_safe

        mock_safe_exec.side_effect = lambda code, results, **kwargs: results.update(
            {"submission_result": None, "answer_result": None, "error": None, "comparison": False}
        )

        attempt_safe(
            dataset="social",
            answer_query="SELECT * FROM Highschooler",
            verify_query="SELECT COUNT(*)",
            modification_query="DELETE FROM Friend",
            is_ordered=False,
            query="SELECT name FROM Highschooler",
        )

        call_args = mock_safe_exec.call_args
        results_dict = call_args[0][1]
        self.assertEqual(results_dict["dataset"], "social")
        self.assertEqual(results_dict["answer_query"], "SELECT * FROM Highschooler")
        self.assertEqual(results_dict["verify_query"], "SELECT COUNT(*)")
        self.assertEqual(results_dict["modification_query"], "DELETE FROM Friend")
        self.assertFalse(results_dict["is_ordered"])
        self.assertEqual(results_dict["query"], "SELECT name FROM Highschooler")


class TestScorable(TestCase):
    """Test scoring methods on the SqlGrader XBlock."""

    def setUp(self):
        self.xblock = make_an_xblock(weight=10)

    def test_max_score_equals_weight(self):
        """max_score should return the configured weight."""
        self.assertEqual(self.xblock.max_score(), 10)

    def test_get_score_returns_none_before_submission(self):
        """Before any answer is submitted, get_score returns None."""
        self.assertIsNone(self.xblock.get_score())

    def test_has_submitted_answer_false_initially(self):
        """Before scoring, has_submitted_answer is False."""
        self.assertFalse(self.xblock.has_submitted_answer())

    def test_set_score_updates_score_field(self):
        """set_score should extract raw_earned from a Score object."""
        score = Score(raw_earned=0.75, raw_possible=1.0)
        self.xblock.set_score(score)
        self.assertEqual(self.xblock.score, 0.75)

    def test_get_score_after_set(self):
        """After setting a score, get_score should return the numeric value."""
        score = Score(raw_earned=1.0, raw_possible=1.0)
        self.xblock.set_score(score)
        self.assertEqual(self.xblock.get_score(), 1.0)

    def test_has_submitted_answer_true_after_scoring(self):
        """After setting a score, has_submitted_answer returns True."""
        score = Score(raw_earned=0.0, raw_possible=1.0)
        self.xblock.set_score(score)
        self.assertTrue(self.xblock.has_submitted_answer())

    @patch("sql_grader.mixins.grading.attempt_safe")
    def test_calculate_score_correct_answer(self, mock_attempt):
        """
        calculate_score should return a Score with raw_earned=1.0
        when the comparison is True.
        """
        mock_attempt.return_value = (
            [(1, "data")],  # actual
            [(1, "data")],  # expected
            None,  # error
            True,  # comparison
        )
        score = self.xblock.calculate_score()
        self.assertEqual(score.raw_earned, 1.0)
        self.assertEqual(score.raw_possible, 1.0)

    @patch("sql_grader.mixins.grading.attempt_safe")
    def test_calculate_score_wrong_answer(self, mock_attempt):
        """
        calculate_score should return a Score with raw_earned=0.0
        when the comparison is False.
        """
        mock_attempt.return_value = (
            [(2, "wrong")],  # actual
            [(1, "data")],  # expected
            None,  # error
            False,  # comparison
        )
        score = self.xblock.calculate_score()
        self.assertEqual(score.raw_earned, 0.0)
        self.assertEqual(score.raw_possible, 1.0)

    @patch("sql_grader.mixins.grading.attempt_safe")
    def test_calculate_score_with_error(self, mock_attempt):
        """
        When attempt_safe returns an error and comparison is None/False,
        score should be 0.
        """
        mock_attempt.return_value = (None, None, "syntax error", False)
        score = self.xblock.calculate_score()
        self.assertEqual(score.raw_earned, 0.0)


class TestXBlockDataMixinContext(TestCase):
    """Test the provide_context method of XBlockDataMixin."""

    def setUp(self):
        self.xblock = make_an_xblock(
            display_name="Test SQL",
            prompt="Write a query",
            weight=5,
        )

    def test_provide_context_includes_display_fields(self):
        """The template context should include display_name and prompt."""
        context = self.xblock.provide_context({})
        self.assertEqual(context["display_name"], "Test SQL")
        self.assertEqual(context["prompt"], "Write a query")

    def test_provide_context_includes_score_info(self):
        """The context should include max_score and score_weighted fields."""
        context = self.xblock.provide_context({})
        self.assertEqual(context["max_score"], 5)
        self.assertEqual(context["score_weighted"], 0)

    def test_provide_context_with_none(self):
        """provide_context should handle None input gracefully."""
        context = self.xblock.provide_context(None)
        self.assertIsInstance(context, dict)
        self.assertIn("display_name", context)
