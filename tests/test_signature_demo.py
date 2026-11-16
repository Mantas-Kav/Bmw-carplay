"""Tests for the educational HMAC demonstration."""
import unittest
from signature_demo import sign_example, verify_example

class SignatureDemoTests(unittest.TestCase):
    def test_unchanged_message_verifies(self):
        key = b"test-secret"
        msg = b"demo-data"
        self.assertTrue(verify_example(key, msg, sign_example(key, msg)))

    def test_changed_message_fails(self):
        key = b"test-secret"
        signature = sign_example(key, b"demo-data")
        self.assertFalse(verify_example(key, b"changed-data", signature))

    def test_wrong_key_fails(self):
        signature = sign_example(b"key-one", b"demo-data")
        self.assertFalse(verify_example(b"key-two", b"demo-data", signature))

if __name__ == "__main__":
    unittest.main()
