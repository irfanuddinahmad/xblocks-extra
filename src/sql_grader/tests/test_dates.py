"""
Tests for the EnforceDueDates mixin
"""

import datetime
from unittest import TestCase

from sql_grader.mixins.dates import EnforceDueDates


class MockBlock(EnforceDueDates):
    """Minimal mock that acts like an XBlock with optional due/graceperiod attributes."""

    def __init__(self, due=None, graceperiod=None):
        if due is not None:
            self.due = due
        if graceperiod is not None:
            self.graceperiod = graceperiod


class TestIsPastDue(TestCase):
    """Test the is_past_due method under various date/graceperiod conditions."""

    def test_no_due_date_returns_false(self):
        """When no due date is set, the block is never past due."""
        block = MockBlock()
        self.assertFalse(block.is_past_due())

    def test_future_due_date_returns_false(self):
        """A due date in the future means the block is not past due."""
        future = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        future = future.replace(tzinfo=datetime.UTC)
        block = MockBlock(due=future)
        self.assertFalse(block.is_past_due())

    def test_past_due_date_returns_true(self):
        """A due date in the past means the block is past due."""
        past = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        past = past.replace(tzinfo=datetime.UTC)
        block = MockBlock(due=past)
        self.assertTrue(block.is_past_due())

    def test_past_due_with_graceperiod_still_within_grace(self):
        """
        A due date that just passed but has a grace period extending
        into the future should not be considered past due.
        """
        recently_past = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        recently_past = recently_past.replace(tzinfo=datetime.UTC)
        grace = datetime.timedelta(hours=2)
        block = MockBlock(due=recently_past, graceperiod=grace)
        self.assertFalse(block.is_past_due())

    def test_past_due_with_graceperiod_expired(self):
        """
        A due date in the past with a grace period that has also
        expired should be considered past due.
        """
        long_past = datetime.datetime.utcnow() - datetime.timedelta(days=2)
        long_past = long_past.replace(tzinfo=datetime.UTC)
        grace = datetime.timedelta(hours=1)
        block = MockBlock(due=long_past, graceperiod=grace)
        self.assertTrue(block.is_past_due())

    def test_due_date_without_graceperiod(self):
        """A past due date with no grace period is simply past due."""
        past = datetime.datetime.utcnow() - datetime.timedelta(seconds=10)
        past = past.replace(tzinfo=datetime.UTC)
        block = MockBlock(due=past)
        self.assertTrue(block.is_past_due())
