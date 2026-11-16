#!/usr/bin/env python3
"""Read-only binary inspector for authorized BMW licensing research."""
import argparse
import hashlib
from pathlib import Path


def inspect(path: Path) -> None:
    data = path.read_bytes()
    print(f"File: {path.name}")
    print(f"Size: {len(data)} bytes")
    print(f"SHA-256: {hashlib.sha256(data).hexdigest()}")
    print(f"First 64 bytes: {data[:64].hex(' ')}")
    print("Printable ASCII strings (first 20, at least 6 characters):")
    current = []
    strings = []
    for byte in data + b"\x00":
        if 32 <= byte <= 126:
            current.append(chr(byte))
        else:
            if len(current) >= 6:
                strings.append("".join(current))
            current = []
    for value in strings[:20]:
        print("  " + value[:160])
    print("No FSC validity or signature verification performed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Binary sample to inspect")
    args = parser.parse_args()
    inspect(args.file)
