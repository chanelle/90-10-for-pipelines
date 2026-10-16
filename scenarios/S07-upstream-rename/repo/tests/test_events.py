import unittest
from events import event_day
class TestEvents(unittest.TestCase):
    def test_day(self):
        self.assertEqual(event_day("2026-10-15T09:00:00"), "2026-10-15")
