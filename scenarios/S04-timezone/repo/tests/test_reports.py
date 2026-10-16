import sys, unittest
sys.path.insert(0, "src")
from reports import report_date
class TestReports(unittest.TestCase):
    def test_late_night_order_counts_for_previous_day(self):
        # 2026-03-01 03:30 UTC is 2026-02-28 22:30 in New York (business time zone)
        self.assertEqual(report_date(1772335800), "2026-02-28")
