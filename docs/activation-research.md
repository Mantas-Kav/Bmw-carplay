# NBT EVO activation research

## Scope

Initial focus: NBT EVO ID5/ID6. Compatibility depends on hardware, software, installed features, Wi-Fi capability, and licensing status. A firmware string by itself cannot establish that a specific car can be activated.

## Observed example

- Firmware: `NBTevo_Y21432J`
- Family: Y
- I-level listed by third-party table: `2111`
- SWFL listed by third-party table: `007_039_008`
- Third-party claims: split-screen and full-screen CarPlay possible; ENET method offered; USB method not offered.
- Evidence status: **third-party provider claim, not independently tested**.

Source: https://autonavi.ee/tarkvaraversiooni-juhend/?lang=en

Another provider also describes Y-family ENET activation:
https://beamerflash.com/product/bmw-mini-carplay-activation/

## Licensing vs installation

- FSC authorization is conceptually distinct from ordinary feature coding.
- An FSC-related file is not necessarily an authorized, valid BMW license.
- A USB `.bin` filename alone does not tell us its internal format or whether it contains executable code, a license, or configuration.
- ENET is a communication/installation path, not a license-generation mechanism.
- Third-party installers may rely on undocumented modifications; their commercial and legal suitability is unverified.
- A read-only binary inspector cannot verify BMW cryptographic signatures or produce valid activation codes.

## Questions to resolve

1. What public technical documentation describes FSC metadata and signature validation?
2. Which hardware prerequisites must be checked in addition to the firmware string?
3. Can an authorized license be issued or transferred through an approved channel?
4. How can a test bench and recovery procedure be established before writing to any head unit?
5. What legal and contractual restrictions affect a commercial service in Lithuania?

## Research safety

Only analyze files obtained with permission. Do not commit private keys, customer VINs, copyrighted firmware images, or proprietary activation packages. Do not run unknown installers on customer vehicles.
