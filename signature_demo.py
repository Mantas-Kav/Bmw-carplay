#!/usr/bin/env python3
"""Educational digital-signature demonstration; not a BMW FSC generator.

Uses HMAC as a simple analogy for authenticity checks. BMW's actual FSC
signature format and trust chain are not implemented here.
"""
import hashlib
import hmac

def sign_example(secret: bytes, message: bytes) -> str:
    return hmac.new(secret, message, hashlib.sha256).hexdigest()

def verify_example(secret: bytes, message: bytes, signature: str) -> bool:
    return hmac.compare_digest(sign_example(secret, message), signature)

def main() -> None:
    secret = b"example-only-not-a-bmw-key"
    message = b"DEMO_FEATURE=CarPlay;DEMO_VIN=EXAMPLE"
    signature = sign_example(secret, message)
    print("Original example verifies:", verify_example(secret, message, signature))
    changed = message.replace(b"CarPlay", b"Navigation")
    print("Modified example verifies:", verify_example(secret, changed, signature))
    print("This is an HMAC analogy, not a BMW FSC implementation.")

if __name__ == "__main__":
    main()
