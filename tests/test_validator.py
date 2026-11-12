import unittest

from ip_checker.validator import is_valid_ip, get_ip_version, check_ip_format, find_duplicate_ips

class TestIPValidator(unittest.TestCase):

    def test_valid_ipv4(self):
        self.assertTrue(is_valid_ip("192.168.1.1"))

    def test_valid_ipv6(self):
        self.assertTrue(is_valid_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334"))

    def test_invalid_ip(self):
        self.assertFalse(is_valid_ip("999.999.999.999"))

    def test_invalid_text(self):
        self.assertFalse(is_valid_ip("sara"))

    def test_ipv4_version(self):
        self.assertEqual(get_ip_version("192.168.1.1"), 4)

    def test_ipv6_version(self):
        self.assertEqual(get_ip_version("2001:0db8:85a3:0000:0000:8a2e:0370:7334"), 6)

    def test_invalid_ip_version(self):
        self.assertIsNone(get_ip_version("sara"))

    def test_empty_input(self):
        self.assertEqual(check_ip_format(""), "Empty input")

    def test_invalid_ip_format(self):
        self.assertEqual(check_ip_format("999.999.999.999"), "Invalid IP format")

    def test_clean_ip_format(self):
        self.assertEqual(check_ip_format(" 192.168.1.10 "), "192.168.1.10")

    def test_find_duplicate_ips(self):
        ips = ["192.168.1.1", "192.168.1.2", "192.168.1.1", "2001:0db8:85a3:0000:0000:8a2e:0370:7334"]

        result = find_duplicate_ips(ips)
        self.assertEqual(result, ["192.168.1.1"])

    def test_find_no_duplicate_ips(self):
        ips = ["192.168.1.10", "2001:0db8:85a3:0000:0000:8a2e:0370:7334"]
        result = find_duplicate_ips(ips)
        self.assertEqual(result, [])

    def test_find_multiple_duplicate_ips(self):
        ips = ["192.168.1.2", "192.168.1.1", "192.168.1.2", "192.168.1.2"]
        result = find_duplicate_ips(ips)
        self.assertEqual(result, ["192.168.1.2"])