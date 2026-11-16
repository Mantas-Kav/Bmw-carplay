#!/usr/bin/env python3
"""Read-only binary inspection utility for authorized research samples."""
import argparse
import hashlib
import math
import zipfile
from collections import Counter
from pathlib import Path

SIGNATURES = (
    (b"PK\x03\x04", "ZIP archive"),
    (b"\x7fELF", "ELF executable"),
    (b"MZ", "Windows PE/DOS executable"),
    (b"\x1f\x8b", "GZIP stream"),
    (b"\xfd7zXZ\x00", "XZ stream"),
)

def entropy(data: bytes) -> float:
    """Shannon entropy in bits per byte, 0.0 for empty input."""
    if not data:
        return 0.0
    counts = Counter(data)
    return -sum((count / len(data)) * math.log2(count / len(data))
                for count in counts.values())

def inspect(path: Path) -> None:
    data = path.read_bytes()
    print(f"File: {path.name}")
    print(f"Size: {len(data)} bytes")
    print(f"SHA-256: {hashlib.sha256(data).hexdigest()}")
    print(f"First 64 bytes: {data[:64].hex(' ')}")
    print(f"Shannon entropy: {entropy(data):.3f} bits/byte")
    matches = [label for signature, label in SIGNATURES if data.startswith(signature)]
    print(f"Recognized header: {', '.join(matches) if matches else 'unknown'}")
    print(f"ZIP archive: {'yes' if zipfile.is_zipfile(path) else 'no'}")
    print("Printable ASCII strings (first 20, at least 6 characters):")
    current = []
    found = []
    for byte in data + b"\x00":
        if 32 <= byte <= 126:
            current.append(chr(byte))
        else:
            if len(current) >= 6:
                found.append("".join(current))
            current = []
    for value in found[:20]:
        print("  " + value[:160])
    print("No FSC validity or signature verification performed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Local binary sample to inspect")
    args = parser.parse_args()
    inspect(args.file)
