#!/usr/bin/env python3
"""Read-only BMW FSC-related file triage. No BMW license validation or activation."""
import argparse
import json
from pathlib import Path
import re

MAX_BYTES = 8 * 1024 * 1024

def inspect_bytes(data: bytes, filename: str = "sample") -> dict:
    suffix = Path(filename).suffix.lower()
    result = {"type": "unknown", "size_bytes": len(data), "valid_bmw_fsc": "not_checked"}
    if len(data) > MAX_BYTES:
        result["error"] = "file too large for offline inspection"
        return result
    if data.startswith(b"PK\x5cx03\x5cx04"):
        result["type"] = "zip_container"
    elif data.lstrip().startswith(b"<?xml") or (data.lstrip().startswith(b"<") and suffix == ".xml"):
        result["type"] = "xml_candidate"
        result["note"] = "XML contents intentionally not displayed; XML is not proof of a valid FSC"
    elif suffix == ".der" and data[:1] == b"\x5cx30":
        result["type"] = "asn1_der_candidate"
        result["note"] = "SEQUENCE tag detected only; DER structure/signature not validated"
    elif suffix == ".fsc":
        result["type"] = "opaque_fsc_candidate"
        result["note"] = "No verified NBT EVO FSC field layout available; bytes not interpreted"
    elif suffix == ".sig":
        result["type"] = "opaque_signature_candidate"
    else:
        result["note"] = "No supported identification rule"
    return result

def inspect_file(path: Path) -> dict:
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    return inspect_bytes(data, path.name)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="File you have permission to inspect")
    args = parser.parse_args()
    print(json.dumps(inspect_file(args.file), indent=2))

if __name__ == "__main__":
    main()
