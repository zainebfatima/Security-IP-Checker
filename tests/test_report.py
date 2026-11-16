import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from ip_checker.report import generate_report

class TestIPReport(unittest.TestCase):

    def test_generate_report(self):
        test_ips = ["8.8.8.8", "2001:4860:4860::8888"]
        test_flagged = ["8.8.8.8"]

        with TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test_report.txt"

            with patch("ip_checker.report.load_records", return_value=(test_ips, test_flagged)):
                with patch("ip_checker.report.REPORT_FILE", test_file):
                    generate_report()

            with open(test_file, "r") as file:
                report = file.read()

        self.assertIn("Total IPs: 2", report)
        self.assertIn("Flagged IPs: 1", report)
        self.assertIn("Unflagged IPs: 1", report)
        self.assertIn("IPv4 Addresses: 1", report)
        self.assertIn("IPv6 Addresses: 1", report)