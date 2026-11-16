"""Tests using synthetic binary samples only."""
import hashlib
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from inspector import inspect


class InspectorTests(unittest.TestCase):
    def test_synthetic_sample(self):
        payload = b"\x00\x01TEST_SAMPLE_123\x00\xff"
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.bin"
            path.write_bytes(payload)
            output = io.StringIO()
            with redirect_stdout(output):
                inspect(path)
            report = output.getvalue()
            self.assertIn(f"Size: {len(payload)} bytes", report)
            self.assertIn(hashlib.sha256(payload).hexdigest(), report)
            self.assertIn("TEST_SAMPLE_123", report)
            self.assertIn("No FSC validity or signature verification", report)

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "empty.bin"
            path.write_bytes(b"")
            output = io.StringIO()
            with redirect_stdout(output):
                inspect(path)
            self.assertIn("Size: 0 bytes", output.getvalue())


if __name__ == "__main__":
    unittest.main()
