import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from ip_checker.database import (
    create_table,
    insert_ip,
    get_all_records,
    update_flag,
    delete_ip
)

class TestIPDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_db = Path(self.temp_dir.name) / "test_ip_records.db"

        self.db_patcher = patch("ip_checker.database.DB_FILE", self.test_db)
        self.db_patcher.start()

        create_table()

    def tearDown(self):
        self.db_patcher.stop()
        self.temp_dir.cleanup()

    def test_insert_and_get_records(self):
        insert_ip("8.8.8.8")

        records = get_all_records()

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][1], "8.8.8.8")
        self.assertEqual(records[0][2], 0)

    def test_update_flag(self):
        insert_ip("8.8.8.8")

        update_flag("8.8.8.8", 1)

        records = get_all_records()

        self.assertEqual(records[0][2], 1)

    def test_delete_ip(self):
        insert_ip("8.8.8.8")

        delete_ip("8.8.8.8")

        records = get_all_records()

        self.assertEqual(len(records), 0)