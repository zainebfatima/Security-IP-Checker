import unittest
from ip_checker.storage import save_records, load_records, export_to_csv

class TestIPStorage(unittest.TestCase):
    def test_save_and_load_records(self):
        test_ips = ["8.8.8.8", "1.1.1.1"]
        test_flagged = ["8.8.8.8"]

        from pathlib import Path
        from tempfile import TemporaryDirectory
        from unittest.mock import patch

        with TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test_records.json"

            with patch("ip_checker.storage.DATA_FILE", test_file):
                save_records(test_ips, test_flagged)
                loaded_ips, loaded_flagged = load_records()

        self.assertEqual(loaded_ips, test_ips)
        self.assertEqual(loaded_flagged, test_flagged)

    def test_export_to_csv(self):
        from unittest.mock import mock_open, patch

        test_ips = ["8.8.8.8", "1.1.1.1"]
        test_flagged = ["8.8.8.8"]

        mock_file = mock_open()

        with patch("builtins.open", mock_file):
            export_to_csv(test_ips, test_flagged)

        written_data = "".join(
            call.args[0] for call in mock_file().write.call_args_list
        )

        self.assertIn("IP Address,Flagged", written_data)
        self.assertIn("8.8.8.8,Yes", written_data)
        self.assertIn("1.1.1.1,No", written_data)