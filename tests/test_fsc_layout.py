import unittest
from fsc_layout import parse_fsc, FSC_SIZE

class LayoutTests(unittest.TestCase):
    def test_synthetic_carplay(self):
        data = bytearray(FSC_SIZE)
        data[:2] = bytes([1, 1])
        data[2:4] = (0x0143).to_bytes(2, "big")
        data[4:6] = (1).to_bytes(2, "big")
        data[34:43] = b"123456789"
        out = parse_fsc(bytes(data))
        self.assertEqual(out["application_number"], "0x0143")
        self.assertEqual(out["upgrade_index"], 1)
        self.assertNotIn("123456789", str(out))
        self.assertFalse(out["signature_verified"])

    def test_rejects_short_file(self):
        with self.assertRaises(ValueError):
            parse_fsc(bytes(FSC_SIZE - 1))

    def test_rejects_long_file(self):
        with self.assertRaises(ValueError):
            parse_fsc(bytes(FSC_SIZE + 1))

if __name__ == "__main__":
    unittest.main()
