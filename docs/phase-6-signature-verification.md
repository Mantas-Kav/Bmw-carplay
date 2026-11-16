# Phase 6 — offline FSC signature verification

Implementation: `fsc_verify.py`, tests: `tests/test_fsc_verify.py`.

The algorithm follows the format **reported** in evocode's `evocode/fsc.py`: 60-byte body, 128-byte RSA signature, exponent 3, MD5 DigestInfo, PKCS#1 v1.5 padding. Source: https://github.com/FreZZZeR/evocode/blob/main/evocode/fsc.py

This is a read-only verifier, not a signer or activation tool. It requires a public modulus supplied by the operator and deliberately does not attempt to recover, install, or replace head-unit trust anchors.

A valid result means only that the file matches the *supplied public modulus*. It does not establish BMW OEM authorization, vehicle compatibility, or that a head unit trusts the key.

Tests include rejection paths and one synthetic positive RSA case. No customer VIN, BMW firmware, private signing key, or real FSC sample is stored in this repository.

**Next evidence gate:** obtain a permitted genuine sample and its legitimately available public verification key, then compare offline results. Do not sell activations based on synthetic tests.
