import unittest
from fsc_inspector import inspect_bytes, MAX_BYTES

class FscInspectorTests(unittest.TestCase):
    def test_opaque_fsc(self):
        info = inspect_bytes(b"arbitrary", "example.fsc")
        self.assertEqual(info["type"], "opaque_fsc_candidate")
        self.assertEqual(info["valid_bmw_fsc"], "not_checked")

    def test_der_candidate(self):
        self.assertEqual(inspect_bytes(bytes([0x30, 0x03, 0x01]), "sample.der")["type"], "asn1_der_candidate")

    def test_xml_candidate(self):
        self.assertEqual(inspect_bytes(b"<?xml version='1.0'?><test/>", "sample.xml")["type"], "xml_candidate")

    def test_zip(self):
        self.assertEqual(inspect_bytes(bytes([0x50, 0x4b, 0x03, 0x04]), "sample.zip")["type"], "zip_container")

    def test_oversize(self):
        self.assertIn("error", inspect_bytes(b"X" * (MAX_BYTES + 1), "sample.fsc"))

if __name__ == "__main__":
    unittest.main()
