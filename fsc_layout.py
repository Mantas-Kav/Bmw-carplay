#!/usr/bin/env python3
"""Offline, read-only parser for the 188-byte FSC layout documented by evocode.

Unverified against BMW hardware. Does not validate signatures or activate features.
Do not publish output containing real vehicle identifiers.
"""
import argparse
import json
from pathlib import Path

BODY_SIZE = 60
SIGNATURE_SIZE = 128
FSC_SIZE = BODY_SIZE + SIGNATURE_SIZE

def parse_fsc(data: bytes) -> dict:
    if len(data) != FSC_SIZE:
        raise ValueError(f"Expected exactly {FSC_SIZE} bytes, got {len(data)}")
    body = data[:BODY_SIZE]
    appno = int.from_bytes(body[2:4], "big")
    return {
        "format": "evocode_reported_188_byte_layout",
        "size_bytes": len(data),
        "version_hex": body[:2].hex(),
        "application_number": f"0x{appno:04X}",
        "upgrade_index": int.from_bytes(body[4:6], "big"),
        "signature_bytes_present": len(data[BODY_SIZE:]) == SIGNATURE_SIZE,
        "signature_verified": False,
        "bmw_compatibility_verified": False,
        "vehicle_identifier_redacted": True,
    }

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path)
    args = ap.parse_args()
    with args.path.open("rb") as f:
        data = f.read(FSC_SIZE + 1)
    print(json.dumps(parse_fsc(data), indent=2))

if __name__ == "__main__":
    main()
