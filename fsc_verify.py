#!/usr/bin/env python3
"""Offline-only verification of the evocode-reported 188-byte FSC signature layout.

Checks RSA e=3, PKCS#1 v1.5 and MD5 DigestInfo against a *supplied* public
modulus. This does NOT establish that any BMW head unit trusts that modulus.
No vehicle communication, signing, firmware patching, or key extraction.
"""
import argparse
import hashlib
import json
from pathlib import Path

BODY_LEN = 60
SIG_LEN = 128
FSC_LEN = BODY_LEN + SIG_LEN
DIGEST_INFO_PREFIX = bytes.fromhex("3020300c06082a864886f70d020505000410")

def verify_fsc(data: bytes, modulus: int) -> dict:
    result = {"signature_valid_for_supplied_key": False,
              "bmw_head_unit_trust_verified": False}
    if len(data) != FSC_LEN:
        return {**result, "reason": "invalid_file_length"}
    if modulus <= 0 or modulus.bit_length() > 1024 or modulus.bit_length() < 1000:
        return {**result, "reason": "invalid_modulus_size"}
    body, signature = data[:BODY_LEN], int.from_bytes(data[BODY_LEN:], "big")
    if signature >= modulus:
        return {**result, "reason": "signature_out_of_range"}
    decoded = pow(signature, 3, modulus).to_bytes(SIG_LEN, "big")
    expected = (bytes([0, 1]) + bytes([255]) * (SIG_LEN - 3 - len(DIGEST_INFO_PREFIX) - 16)
                + bytes([0]) + DIGEST_INFO_PREFIX + hashlib.md5(body).digest())
    if decoded != expected:
        return {**result, "reason": "signature_mismatch"}
    return {**result, "signature_valid_for_supplied_key": True,
            "reason": "signature_matches_supplied_key"}

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file", type=Path, help="Permitted local FSC sample")
    ap.add_argument("--modulus-hex", required=True, help="Public RSA modulus (hex); never a private key")
    args = ap.parse_args()
    with args.file.open("rb") as stream:
        data = stream.read(FSC_LEN + 1)
    try:
        modulus = int(args.modulus_hex.removeprefix("0x"), 16)
    except ValueError:
        ap.error("modulus must be hexadecimal")
    print(json.dumps(verify_fsc(data, modulus), indent=2))

if __name__ == "__main__":
    main()
