import hashlib
import unittest
from fsc_verify import verify_fsc, BODY_LEN, SIG_LEN, DIGEST_INFO_PREFIX

# Tiny deterministic RSA toy example is not suitable for 1024-bit FSC padding.
# Instead verify rejection cases with synthetic 188-byte inputs and a 1024-bit
# modulus; no BMW files or keys are used.
MODULUS = (1 << 1023) + 643

class VerifyTests(unittest.TestCase):
    def test_wrong_length(self):
        self.assertEqual(verify_fsc(b"x", MODULUS)["reason"], "invalid_file_length")

    def test_invalid_modulus(self):
        self.assertEqual(verify_fsc(bytes(188), 17)["reason"], "invalid_modulus_size")

    def test_out_of_range_signature(self):
        sample = bytes(BODY_LEN) + MODULUS.to_bytes(SIG_LEN, "big")
        self.assertEqual(verify_fsc(sample, MODULUS)["reason"], "signature_out_of_range")

    def test_mismatch(self):
        result = verify_fsc(bytes(188), MODULUS)
        self.assertEqual(result["reason"], "signature_mismatch")
        self.assertFalse(result["bmw_head_unit_trust_verified"])

    def test_correct_signature_with_synthetic_rsa_key(self):
        # Deterministic RSA key is constructed at runtime from two probable primes
        # for a test only, without network access or BMW-specific key material.
        from random import Random
        rng = Random(2026)
        def prime(bits):
            while True:
                n = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
                if n % 3 != 2:
                    continue
                if all(n % p for p in (3,5,7,11,13,17,19,23,29,31,37)):
                    # Miller-Rabin fixed bases adequate for test fixture generation
                    d = n - 1
                    s = 0
                    while d % 2 == 0:
                        s += 1
                        d //= 2
                    if all((lambda a: (lambda x: x == 1 or x == n-1 or any(
                        (lambda y: y == n-1)(pow(a, d * (1 << r), n))
                        for r in range(1, s)))(pow(a, d, n)))(a)
                        for a in (2,3,5,7,11,13,17,19,23,29,31,37)):
                        return n
        p, q = prime(512), prime(512)
        while p == q:
            q = prime(512)
        n = p*q
        d = pow(3, -1, (p-1)*(q-1))
        body = bytes(range(BODY_LEN))
        envelope = (bytes([0,1]) + bytes([255]) * (SIG_LEN - 3 - len(DIGEST_INFO_PREFIX) - 16)
                    + bytes([0]) + DIGEST_INFO_PREFIX + hashlib.md5(body).digest())
        signature = pow(int.from_bytes(envelope, "big"), d, n).to_bytes(SIG_LEN, "big")
        result = verify_fsc(body + signature, n)
        self.assertTrue(result["signature_valid_for_supplied_key"])
        self.assertFalse(result["bmw_head_unit_trust_verified"])

if __name__ == "__main__":
    unittest.main()
